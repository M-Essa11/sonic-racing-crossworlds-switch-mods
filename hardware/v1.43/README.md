# Sonic Racing: CrossWorlds v1.43 — Atmosphere patches

I tested both patches together on my Switch Lite running Atmosphere, and they
work well. This package is for the original Switch version of CrossWorlds v1.43.

## Exact target

- Game update: **v1.43**
- Title ID: `01006E001823C000`
- Short Build ID: `CF6A61882F2ADE94`
- Build ID prefix: `CF6A61882F2ADE943495CF2918A73E07`

## Install

1. Back up and disable conflicting Sonic FPS/resolution patches, old graphics
   cheats and RomFS graphics overrides. Do not rename patches from another build.
2. Extract the ZIP and merge its `atmosphere` folder into the SD card root.
3. Keep both `.ips` files in their separate folders shown below.
4. Fully close and reopen the game. Test an offline race first.

```text
SD:/atmosphere/exefs_patches/
├── Sonic Racing CW v1.43 - Static 60FPS/
│   └── CF6A61882F2ADE943495CF2918A73E07.ips
└── Sonic Racing CW v1.43 - Resolution/
    └── CF6A61882F2ADE943495CF2918A73E07.ips
```

The matching filenames identify the same executable. One file does not replace
the other: their parent folders differ. Atmosphere loads both patches. These
patches do not require a SaltySD or FPSLocker game configuration.

For a staged test, install only Static 60FPS first, test a race, then add Resolution.
If you already installed the experimental v1.43 package, move its `60FPS Candidate`
and `Resolution Test` folders out of `exefs_patches` before installing these renamed
folders. Patch bytes are unchanged from the tested candidate; avoid duplicates.

## A quick note on performance

The resolution patch targets 1080p docked / 720p handheld. Performance can vary
by track and settings, so try 60 FPS on its own first, then add resolution.
If the game slows down or FPS drops, remove the resolution patch and compare.

I tested on Switch Lite; I haven’t tested every mode or other Switch models.
This is a static FPS patch, so it does not guarantee a locked 60 FPS everywhere.
Actual internal resolution hasn’t been measured. The technical checks and porting
notes are in `validation.json`.

## Uninstall / rollback

Remove the `Sonic Racing CW v1.43 - Resolution` folder to undo resolution only.
Remove both named v1.43 folders to undo both patches. Fully relaunch the game.

## Static verification

The v1.43 dump's Build ID and all three decompressed NSO section hashes were
verified. All 37 original byte sequences were checked. Both IPS32 files were
decoded back and checked for offsets, payloads, +0x100 NSO header adjustment and
non-overlap. The published files are byte-identical to the user-tested candidates.
Only patches and documentation are included; no game binaries or keys.

## Credits and rights

Original patch behavior: [Fl4sh9174](https://github.com/Fl4sh9174) —
[upstream mods](https://github.com/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods).
[Support Fl4sh](https://ko-fi.com/Fl4sh9174).

Ported and tested by M-Essa11.
This is independent work, not an official Fl4sh release or endorsement. Original
authors retain their rights; no new license to their work is granted here.
