# Sonic Racing: CrossWorlds v1.41 — Experimental Switch Mods

![Experimental](https://img.shields.io/badge/status-experimental-orange)
![Game version](https://img.shields.io/badge/game-v1.41-blue)

Experimental community ports of **Fl4sh9174's earlier-version patches** for the Nintendo Switch version of Sonic Racing: CrossWorlds. Includes **60 FPS, 1080p, improved FOV, and improved level of detail**.

**Initial user testing in Eden on Windows reports that the patches work.** Published as a regular release, with the experimental label retained while community testing expands. Feedback and bug reports are welcome, especially for timing, different game modes, and long-session stability. This is an independent port, not an official Fl4sh release or endorsement.

## Download

Download the mod ZIP from the [experimental release](https://github.com/M-Essa11/sonic-racing-crossworlds-switch-mods/releases/tag/v1.41-experimental.1).

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
| 1920x1080 | Ports the resolution adjustment; original patch describes 1080p docked / 720p handheld |
| Improved FOV | Multiplies the affected FOV value by 1.375 |
| Improved Level of Detail | Ports the original LOD adjustment |

## Install in Eden

1. Make sure the game launches normally on v1.41 without mods.
2. Right-click the game and choose **Open Mod Data Location**.
3. Extract the four bracket-named mod folders from the release ZIP directly into that directory.
4. Disable old versions and conflicting graphics/FPS mods in the game's configuration.
5. Enable **60 FPS alone first**, test a race, then add the other mods individually.

Expected layout:

```text
<game mod directory>/
  [60 FPS V1.41 Experimental]/
    exefs/
      1.41.pchtxt
```

For a repository checkout, copy the folders **inside `mods/`**, not the `mods` parent itself. Uninstall by disabling the entries or removing only these four folders.

## Troubleshooting and testing

- Check the game update and Build ID if a patch is ignored.
- Check for other executable overrides if the game black-screens or the Build ID looks wrong. During development, an existing `sdmc/atmosphere/contents/01006E001823C000/exefs/main` override replaced the updated executable. Backing up and removing that override resolved the launch issue in the test setup. These patches do not require a replacement `main` file.
- Test race speed, timers, physics, cutscenes, camera behavior, split-screen, and docked/handheld modes. Disable a patch if it causes problems.
- Report emulator version, game Build ID, enabled mods, reproduction steps, and observed versus expected behavior in [Issues](https://github.com/M-Essa11/sonic-racing-crossworlds-switch-mods/issues). Do not attach game executables or keys.

## How the port was checked

Six code sites were located using unique 128-byte instruction patterns with relocation-sensitive fields masked. The original instruction bytes matched at every patched location. The FPS table had a unique exact 132-byte match. The FOV branch was recalculated to matching three-instruction padding after a return. All **43 writes** were checked against the target executable before packaging.

The reference executable had a zeroed Build ID and unverified provenance; it was useful because its code matched the original patch sites. This limits certainty and is another reason the release remains experimental. See [`validation.json`](validation.json) for offsets, original bytes, replacement bytes, target hash, and testing status. Static checks do not establish gameplay correctness.

## Credits and rights

Original patch work: **[Fl4sh9174](https://github.com/Fl4sh9174)** — [upstream mod repository](https://github.com/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods). [Support Fl4sh on Ko-fi](https://ko-fi.com/Fl4sh9174).

This repository provides a community v1.41 port maintained by M-Essa11, prepared with AI-assisted binary analysis. Credit for the original mod behavior belongs to Fl4sh9174.

No upstream license was detected when preparing this release. This repository does not claim to relicense the original patch work or grant rights beyond those held by the respective authors. Game names and trademarks belong to their owners.

Only patch text and documentation are distributed. No game executables, game assets, firmware, keys, saves, or personal emulator logs are included.
