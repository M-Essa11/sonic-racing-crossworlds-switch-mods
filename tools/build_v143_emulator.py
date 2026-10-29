"""Build v1.43 emulator patches after checking every original write.

Usage: python tools/build_v143_emulator.py --exefs "SRC 1.43"
Requires lz4 and capstone. Never distributes executable dumps.
"""
from pathlib import Path
import argparse
import array
import hashlib
import json
import re
import shutil
import struct
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".analysis-tools"))
import lz4.block
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

MAIN_BID = "CF6A61882F2ADE943495CF2918A73E07"
SDK_BID = "AD9EE4518B1D8CA811FBDF35FC4F26D5FC1ADA57"
MAIN_SHA = "0bc75b9418f8b0ce95db6eb79a5b67473a9e4924fd44464254df6bf8199cc35f"
SDK_SHA = "085c580b2e172404c48f9ed84caf7a47895269c1df664fe4a0cad02b880243e2"
FOV_CAVE = 0x04C0A974
UW_CAVE = 0x04C0A6D4
CS = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load_nso(path, expected_bid, expected_sha):
    raw = path.read_bytes()
    assert raw[:4] == b"NSO0", f"Not an NSO: {path.name}"
    assert sha(raw) == expected_sha, f"Unexpected {path.name} hash; do not use this build"
    assert raw[0x40:0x60].hex().upper().rstrip("0") == expected_bid.rstrip("0")
    flags = struct.unpack_from("<I", raw, 12)[0]
    segments = []
    for i in range(3):
        offset, address, size = struct.unpack_from("<III", raw, 0x10 + i * 16)
        compressed = struct.unpack_from("<I", raw, 0x60 + i * 4)[0]
        data = lz4.block.decompress(raw[offset:offset + compressed], uncompressed_size=size) \
            if flags & (1 << i) else raw[offset:offset + size]
        assert len(data) == size
        expected_digest = raw[0xA0 + 32*i:0xC0 + 32*i]
        if flags & (1 << (i + 3)):
            assert hashlib.sha256(data).digest() == expected_digest
        segments.append((address, data))
    memory = bytearray(max(address + len(data) for address, data in segments))
    for address, data in segments:
        memory[address:address + len(data)] = data
    return memory, segments[0][0] + len(segments[0][1])

def branch(pc, target):
    delta = target - pc
    assert delta % 4 == 0 and -(1 << 27) <= delta < (1 << 27)
    return struct.pack("<I", 0x14000000 | ((delta >> 2) & 0x3FFFFFF))

def adrp(pc, target, register):
    pages = ((target & ~4095) - (pc & ~4095)) >> 12
    assert -(1 << 20) <= pages < (1 << 20)
    immediate = pages & 0x1FFFFF
    return struct.pack("<I", 0x90000000 | ((immediate & 3) << 29) |
                       ((immediate >> 2) << 5) | register)

def relocated(old):
    if 0x05CEDFB0 <= old <= 0x05CEE030:
        return old + 0x2000
    return {
        0x016F9FD4: 0x016F95D4,
        0x04BD191C: 0x04BD2D9C,
        0x03F6DC7C: 0x03F6EC3C,
        0x00732A48: 0x00732A48,
        0x00E42FD4: 0x00E43054,
        0x00E42FD8: 0x00E43058,
        0x04C094F4: FOV_CAVE,
        0x04C094F8: FOV_CAVE + 4,
        0x04C094FC: FOV_CAVE + 8,
        0x00DE89C8: 0x00DE89B8,
        0x00A83994: 0x00A83994,
        0x052E7D04: UW_CAVE,
        0x052E7D08: UW_CAVE + 4,
        0x052E7D0C: UW_CAVE + 8,
        0x05AFD7D4: 0x05AFF7B4,
        **{x: x for x in range(0x009B5AA8, 0x009B5AC4, 4)},
        0x01A5DC10: 0x01A5DE30,
        0x01A5DC14: 0x01A5DE34,
        0x00EB0224: 0x00EB02A4,
        0x00EB0228: 0x00EB02A8,
        0x00F47A00: 0x00F47A80,
        0x00F47A04: 0x00F47A84,
    }[old]

def check_sites(memory, text_end):
    def expect(address, data):
        assert memory[address:address+len(data)] == data, f"Context mismatch at {address:08X}"
    # FOV setter: unique store-to-camera-field and return sequence.
    setter = bytes.fromhex("003002bdc0035fd6")
    assert memory.count(setter) == 1
    expect(0x00E43054, setter)
    # LOD: verify the setting read and subsequent indirect setter call together.
    expect(0x00DE89B4, bytes.fromhex(
        "00013fd6600640bda8f403b0a06301d1084d42f900013fd66006412d"))
    # Ultrawide aspect/HUD block and constructors.
    expect(0x009B5AA8, bytes.fromhex(
        "ec00005408ad43f91f0119eb41a20054086c82520000088b003040bd"))
    expect(0x00EB02A4, bytes.fromhex("68c7915268fca772684e02b9"))
    expect(0x00F47A80, bytes.fromhex("68c7915268fca772694e41f9284d02b9"))
    expect(0x01A5DE30, bytes.fromhex("69c7915269fca77269c601b9"))
    for cave in (FOV_CAVE, UW_CAVE):
        assert cave + 12 <= text_end
        expect(cave - 4, bytes.fromhex("c0035fd6" + "1f2003d5" * 3))
    # Reject padding that is already a direct branch destination in the original.
    words = array.array("I", memory[:text_end - text_end % 4])
    if sys.byteorder != "little":
        words.byteswap()
    destinations = {x for cave in (FOV_CAVE, UW_CAVE) for x in range(cave, cave+12, 4)}
    def sign(value, width):
        return value - (1 << width) if value & (1 << (width-1)) else value
    for i, word in enumerate(words):
        if word & 0x7C000000 == 0x14000000:  # B / BL
            target = i*4 + sign(word & 0x3FFFFFF, 26)*4
        elif word & 0xFF000010 == 0x54000000 or word & 0x7E000000 == 0x34000000:
            target = i*4 + sign((word >> 5) & 0x7FFFF, 19)*4
        elif word & 0x7E000000 == 0x36000000:
            target = i*4 + sign((word >> 5) & 0x3FFF, 14)*4
        else:
            continue
        assert target not in destinations, f"Original branch targets selected padding at {target:08X}"

def render_patch(bid, name, writes):
    lines = [f"@nsobid-{bid}", "", f"# Sonic Racing: CrossWorlds v1.43 - {name}",
             "# Original patches: Fl4sh9174. v1.43 port: M-Essa11.",
             "# Local test build; gameplay verification pending.", "",
             "@flag print_values", "@flag offset_shift 0x100", "", "@enabled"]
    lines += [f"{x['offset']} {x['replacement'].upper()}" for x in writes]
    lines += ["@stop", "", "# https://github.com/Fl4sh9174", "# https://ko-fi.com/Fl4sh9174", ""]
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exefs", type=Path, required=True)
    args = parser.parse_args()
    memory, text_end = load_nso(args.exefs / "main", MAIN_BID, MAIN_SHA)
    sdk, _ = load_nso(args.exefs / "sdk", SDK_BID, SDK_SHA)
    check_sites(memory, text_end)
    reference = json.loads((ROOT / "tools/v141-reference.json").read_text())
    output = ROOT / "emulator/v1.43"
    mod_root = output / "mods"
    groups = {}
    for change in reference["changes"]:
        module = change.get("module", "main")
        old = int(change["target_offset"], 16)
        address = old if module == "sdk" else relocated(old)
        original = bytes.fromhex(change["original"])
        replacement = bytes.fromhex(change["replacement"])
        if module == "main":
            if old == 0x00E42FD8:
                replacement = branch(address, FOV_CAVE)
            elif old == 0x052E7D04:
                replacement = adrp(address, 0x05AFF7B4, 8)
            elif old == 0x052E7D08:
                replacement = struct.pack("<I", 0xBD400000 | (((0x05AFF7B4 & 4095)//4) << 10) | (8 << 5))
            elif old == 0x052E7D0C:
                replacement = branch(address, 0x00A83998)
        source = sdk if module == "sdk" else memory
        assert source[address:address+len(original)] == original, f"Original bytes differ: {change['mod']} {address:08X}"
        name = change["mod"].replace("V1.41", "V1.43")
        groups.setdefault(name, []).append({
            "module": module, "old_v141_offset": f"{old:08X}", "offset": f"{address:08X}",
            "original": original.hex(), "replacement": replacement.hex(),
        })
    assert len(groups) == 7 and sum(map(len, groups.values())) == 100
    for name, writes in groups.items():
        directory = mod_root / name / "exefs"
        directory.mkdir(parents=True, exist_ok=True)
        for module in ("main", "sdk"):
            selected = [x for x in writes if x["module"] == module]
            if selected:
                (directory / ("v2.pchtxt" if module == "sdk" else "1.43.pchtxt")).write_text(
                    render_patch(SDK_BID if module == "sdk" else MAIN_BID, name, selected), encoding="utf-8")
    archives = []
    for entry in reference["configuration_archives"]:
        source = ROOT / "mods" / entry["mod"] / Path(entry["file"].replace("\\", "/"))
        data = source.read_bytes()
        assert sha(data) == entry["sha256"]
        dest = mod_root / entry["mod"].replace("V1.41", "V1.43") / Path(entry["file"].replace("\\", "/"))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        archives.append({"path": dest.relative_to(output).as_posix(), "sha256": sha(data),
                         "status": "Inherited configuration copied byte-for-byte; v1.43 runtime test pending"})
    report = {
        "version": "1.43", "title_id": "01006E001823C000", "build_id": MAIN_BID,
        "main_sha256": MAIN_SHA, "sdk_build_id": SDK_BID, "sdk_sha256": SDK_SHA,
        "status": "release_user_tested_eden", "runtime_tested": True, "runtime_test_report": "M-Essa11 reports all seven mods working in Eden on Windows, 2026-10-29",
        "original_byte_checks": 100, "mod_count": 7,
        "notes": [
            "60 FPS mapping inherited from the previously hardware-tested v1.43 package; third site was originally inferred without v1.41 code context.",
            "FOV setter is a unique STR S0,[X0,#0x230];RET sequence. Its helper preserves the original store/return after multiplying by 1.375.",
            "LOD instruction relocated by nearby setting-call structure and expected original bytes, without the old executable for full context comparison; effect reported working by M-Essa11 in Eden.",
            "Helpers use verified three-NOP padding after RET; no direct original B/BL/B.cond/CBZ/CBNZ/TBZ/TBNZ targets those slots.",
            "Ultrawide keeps the inherited active FMOV S0,#2.375. The inherited aspect-load helper remains dormant; its address calculation and return are nevertheless relocated correctly.",
            "SDK hash matches the reference SDK. 120 FPS remains static and has known slowdown reports from v1.41; M-Essa11 reports the v1.43 set working in Eden; the historical slowdown limitation remains relevant on other setups.",
            "M-Essa11 reports all seven mods working in Eden. Exact internal resolution has not been instrumented; other emulators and configurations remain unverified.",
        ],
        "patches": groups, "configuration_archives": archives,
    }
    # Read every emitted patch back, and apply its writes independently to a copy.
    for name, expected_writes in groups.items():
        parsed = []
        for file in sorted((mod_root/name/"exefs").glob("*.pchtxt")):
            module = "sdk" if file.name == "v2.pchtxt" else "main"
            content = file.read_text()
            assert f"@nsobid-{SDK_BID if module == 'sdk' else MAIN_BID}" in content
            patched = bytearray(sdk if module == "sdk" else memory)
            for line in content.splitlines():
                match = re.fullmatch(r"([0-9A-F]{8}) ([0-9A-F]+)", line)
                if not match:
                    continue
                address = int(match[1], 16); replacement = bytes.fromhex(match[2])
                expected = next(x for x in expected_writes if x["module"] == module and int(x["offset"],16) == address)
                assert replacement.hex() == expected["replacement"]
                patched[address:address+len(replacement)] = replacement
                parsed.append((module,address))
            for x in expected_writes:
                if x["module"] == module:
                    address = int(x["offset"],16)
                    assert patched[address:address+4].hex() == x["replacement"]
        assert len(parsed) == len(expected_writes) == len(set(parsed))
    fov = groups["[Improved FOV V1.43]"]
    branch_write = next(x for x in fov if x["offset"] == "00E43058")
    instruction = next(CS.disasm(bytes.fromhex(branch_write["replacement"]), 0x00E43058))
    assert instruction.mnemonic == "b" and instruction.op_str == f"#0x{FOV_CAVE:x}"
    (output / "validation.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    readme = output / "README.md"
    assert readme.is_file(), "Create installation/testing README before packaging"
    archive = ROOT / "downloads/Sonic-Racing-CrossWorlds-v1.43-Emulator.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for file in sorted(mod_root.rglob("*")):
            if file.is_file():
                z.write(file, file.relative_to(mod_root).as_posix())
        z.write(readme, "INSTALL.md")
        z.write(output / "validation.json", "validation.json")
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert sum(n.endswith(".pchtxt") for n in z.namelist()) == 8
        assert sum(n.endswith(".pak") for n in z.namelist()) == 2
        assert not any(Path(n).name in {"main", "sdk", "rtld", "main.npdm"} for n in z.namelist())
        for file in mod_root.rglob("*"):
            if file.is_file():
                assert z.read(file.relative_to(mod_root).as_posix()) == file.read_bytes()
    print(json.dumps({"zip": str(archive), "sha256": sha(archive.read_bytes()),
                      "mods": len(groups), "writes_checked": 100, "runtime_tested": True, "runtime_test_report": "M-Essa11 reports all seven mods working in Eden on Windows, 2026-10-29"}, indent=2))

if __name__ == "__main__":
    main()
