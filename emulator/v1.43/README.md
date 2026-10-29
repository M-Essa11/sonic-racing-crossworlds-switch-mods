# Sonic Racing: CrossWorlds v1.43 â€” local emulator test

Ports of Fl4sh9174's patches by M-Essa11. For Eden and compatible Switch emulators.
These files have passed executable-byte and package checks. This full emulator
set has not yet been tested in-game on v1.43.

Game: Nintendo Switch edition, title ID `01006E001823C000`.
Required main Build ID: `CF6A61882F2ADE943495CF2918A73E07`.
The SDK patch additionally targets `AD9EE4518B1D8CA811FBDF35FC4F26D5FC1ADA57`.

## Install

1. Make sure the unmodded game starts on v1.43.
2. In Eden, right-click the game and select **Open Mod Data Location**.
3. Extract the seven bracket-named folders from the ZIP directly into that folder.
4. Disable the old v1.41 mods and any other FPS/resolution/camera overrides.
5. Enable **60 FPS alone** and test a race first. Add the other options one at a time.

Example:

```
<game mod directory>/
  [60 FPS V1.43]/exefs/1.43.pchtxt
  [1920x1080 V1.43]/exefs/1.43.pchtxt
  [Improved FOV V1.43]/exefs/1.43.pchtxt
```

Use **Open Mod Data Location** to confirm the location in your emulator.
Copy the contents of `emulator/v1.43/mods/` when using the source checkout.
The supplied ZIP already puts the seven folders at its top level.

## Options

| Mod | Intended behavior |
| --- | --- |
| 60 FPS | Static 60 FPS timing changes; use only when the emulator can maintain the target. |
| 120 FPS | Static 120 FPS alternative, with both main and SDK patch files. Known slowdown reports exist for the v1.41 equivalent. |
| 1920x1080 | Full resolution percentage; intended 1080p docked / 720p handheld. |
| 3840x2160 | Full resolution percentage plus the inherited 4K configuration PAK. |
| 3440x1440 Ultrawide Adjusted HUD | Inherited ultrawide configuration plus aspect/HUD/camera changes; use a matching viewport and stretch-to-window. |
| Improved FOV | Multiplies the affected camera FOV by 1.375. |
| Improved Level of Detail | Retains Fl4sh's LOD adjustment at its relocated setting site. |

Choose **one FPS option** and **one resolution/aspect option**. FOV and LOD are
separate optional changes. Keep both `1.43.pchtxt` and `v2.pchtxt` inside 120 FPS.
For 4K/ultrawide, start in docked mode and at the emulator's native/1x resolution;
additional emulator resolution scaling can increase the render resolution further.
Effective output/internal resolution still needs to be measured in-game.

## Testing

Try this order:

1. 60 FPS: check race speed, countdown and lap timers, physics and cutscenes.
2. 1080p, then 4K separately: check sharpness and performance.
3. Improved FOV: compare the same camera/racer with it on and off.
4. Improved LOD: compare distant track geometry and object pop-in.
5. Ultrawide alone as the resolution option: check menus, HUD, cutscenes and gameplay.
6. 120 FPS last: check real-time race speed as well as the FPS counter.

If 120 FPS produces slow motion, use 60 FPS. These are static patches, not a
dynamic-FPS implementation. Turning on a higher target does not guarantee it
will run at that speed.

The FOV helper and branch instructions have been rebuilt for v1.43. The LOD site
uses expected original bytes and setting-call context, without the old main for
complete cross-build comparison. The inherited ultrawide helper was dormant in
the previous patch and remains so here. See `validation.json` for those limits.

To uninstall, disable or remove only the seven v1.43 mod folders. No replacement
game executable is needed. Do not copy the ExeFS dumps to the mod directory.

## Credits

Original patches and configuration PAKs: [Fl4sh9174](https://github.com/Fl4sh9174).
[Support Fl4sh](https://ko-fi.com/Fl4sh9174).
v1.43 port and packaging: M-Essa11.

This package contains patch text, two inherited configuration archives and
documentation. It contains no game executables, keys, firmware or saves.
It does not relicense the original patch work.
