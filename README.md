# Sonic Racing: CrossWorlds v1.41 — Experimental Switch Mods

![Release](https://img.shields.io/badge/status-released-green)
![Game version](https://img.shields.io/badge/game-v1.41-blue)

Community ports of **Fl4sh9174's earlier-version patches** for the Nintendo Switch version of Sonic Racing: CrossWorlds. Includes **60 FPS, 120 FPS, 1080p, 4K, 3440×1440 ultrawide with adjusted HUD, improved FOV, and improved level of detail**.

**User testing in Eden on Windows reports that the full set works.** Slow motion has been reported with the 120 FPS option. Feedback and bug reports are welcome. This is an independent port, not an official Fl4sh release or endorsement.

## 120 FPS slowdown

Slow motion has been reported with the 120 FPS option. These are static FPS patches, not a dynamic-FPS solution. If you experience slowdown, try **60 FPS** and report your results. Performance and compatibility vary by system.

## Download

Download the mod ZIP from the [latest release](https://github.com/M-Essa11/sonic-racing-crossworlds-switch-mods/releases/latest).

## Compatibility

| Item | Target |
| --- | --- |
| Game | Sonic Racing: CrossWorlds, Nintendo Switch version |
| Update | v1.41 (as displayed by Eden) |
| Title ID | `01006E001823C000` |
| Build ID | `6455A932B210658FFF0EACCC1D143A22` |
| Reported test environment | Eden on Windows |

These patches target this exact executable build. Other game updates, emulators, and real hardware are unverified. They are not PC-version or Switch 2 Edition mods. Maintaining 60 FPS depends on available performance; this is not a dynamic-FPS implementation.

## Included patches

| Mod | Intended behavior |
| --- | --- |
| 60 FPS | Ports the frame-rate instructions and timing/settings table from the original patch |
| 120 FPS | Higher frame-rate option; requires both included ExeFS patch files; see slowdown note above |
| 3840x2160 / 4K | Resolution patch plus Fl4sh’s original configuration archive |
| 3440x1440 Ultrawide Adjusted HUD | Aspect, menu/cutscene FOV adjustments, and original configuration archive; use stretch-to-window |
| 1920x1080 | Ports the resolution adjustment; original patch describes 1080p docked / 720p handheld |
| Improved FOV | Multiplies the affected FOV value by 1.375 |
| Improved Level of Detail | Ports the original LOD adjustment |

## Install in Eden

1. Make sure the game launches normally on v1.41 without mods.
2. Right-click the game and choose **Open Mod Data Location**.
3. Extract the seven bracket-named mod folders from the release ZIP directly into that directory.
4. Disable old versions and conflicting graphics/FPS mods in the game's configuration.
5. Enable **60 FPS alone first**, test a race, then add the other mods individually.

Expected layout:

```text
<game mod directory>/
  [60 FPS V1.41]/
    exefs/
      1.41.pchtxt
```

**Select only one FPS option (60 or 120) and one resolution/aspect option (1080p, 4K, or ultrawide).** Keep both `1.41.pchtxt` and `v2.pchtxt` inside the 120 FPS mod: the latter patches the unchanged SDK. For ultrawide, use stretch-to-window and a matching viewport. When upgrading, remove or disable the previous folders with the Experimental suffix to avoid duplicate patches.

For a repository checkout, copy the folders **inside `mods/`**, not the `mods` parent itself. Uninstall by disabling the entries or removing only these seven folders.

## Troubleshooting and testing

- Check the game update and Build ID if a patch is ignored.
- Check for other executable overrides if the game black-screens or the Build ID looks wrong. During development, an existing `sdmc/atmosphere/contents/01006E001823C000/exefs/main` override replaced the updated executable. Backing up and removing that override resolved the launch issue in the test setup. These patches do not require a replacement `main` file.
- Test race speed, timers, physics, cutscenes, camera behavior, split-screen, and docked/handheld modes. Disable a patch if it causes problems.
- Report emulator version, game Build ID, enabled mods, reproduction steps, and observed versus expected behavior in [Issues](https://github.com/M-Essa11/sonic-racing-crossworlds-switch-mods/issues). Do not attach game executables or keys.

## How the port was checked

Six code sites were located using unique 128-byte instruction patterns with relocation-sensitive fields masked. The original instruction bytes matched at every patched location. The FPS table had a unique exact 132-byte match. The FOV branch was recalculated to matching three-instruction padding after a return. The additional ultrawide sites were matched with unique instruction contexts; its helper references and return branch were relocated. The 120 FPS SDK executable is byte-identical to the reference version, so its SDK patch is retained. All **100 writes across the seven alternatives** were checked against the relevant target executable before packaging. The two original configuration archives were copied byte-for-byte.

The reference executable had a zeroed Build ID and unverified provenance; it was useful because its code matched the original patch sites. This limits certainty; user testing does not establish compatibility with every game mode or system. See [`validation.json`](validation.json) for offsets, original bytes, replacement bytes, target hash, and testing status. Static checks do not establish gameplay correctness.

## Credits and rights

Original patch work: **[Fl4sh9174](https://github.com/Fl4sh9174)** — [upstream mod repository](https://github.com/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods). [Support Fl4sh on Ko-fi](https://ko-fi.com/Fl4sh9174).

This repository provides a community v1.41 port maintained by M-Essa11, prepared with AI-assisted binary analysis. Credit for the original mod behavior belongs to Fl4sh9174.

No upstream license was detected when preparing this release. This repository does not claim to relicense the original patch work or grant rights beyond those held by the respective authors. Game names and trademarks belong to their owners.

The package contains patch text, Fl4sh’s two configuration PAK archives, and documentation. No game executables, firmware, keys, saves, or personal emulator logs are included.
