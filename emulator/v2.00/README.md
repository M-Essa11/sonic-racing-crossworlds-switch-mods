# CrossWorlds v2.00 emulator mods for Eden

Switch title ID `01006E001823C000`. Main Build ID `D2B8094093CE27AE8C624765C054360F`.

Right-click the game in Eden and choose **Open Mod Data Location**. Extract the bracket-named folders directly there. Disable older CrossWorlds mods and keep emulator speed at 100%. Start at 1x resolution in docked mode. Fully restart the game after changing mods.

- **60 FPS / 120 FPS.** Enable one. Start with 60 FPS alone and check the race clock and driving speed. 120 FPS uses both ExeFS files and can cause slow motion.
- **1920x1080.** Requests 100% render scale in the game profile and disables the identified dynamic override. 1080p docked and 720p handheld are targets pending measurement.
- **3840x2160 / Ultrawide.** Uses the existing configuration PAKs and the new build's fixed scale patch. 4K targets 3840x2160 docked and 1920x1080 handheld. Ultrawide targets 3440x1440 docked and 1720x720 handheld with adjusted HUD. Use a matching viewport and stretch-to-window for ultrawide. Check profile loading and UI in-game.
- **Dynamic Resolution 16ms.** Targets a 16 ms rendering budget when the game's dynamic resolution is active. Test it with 60 FPS and without any fixed-resolution option. FPS timing remains static.
- **Improved FOV / LOD.** Test individually. FOV scales the affected camera field by 1.375. LOD carries over the old setting adjustment.

Use one resolution option at a time, including the dynamic option. The package passed executable and ZIP checks. Tested in Eden by M-Essa11. Render dimensions remain unmeasured. For rollback, disable the bracket-named mod folders and restart.

Original mods and configuration PAKs by Fl4sh9174. v2.00 port by M-Essa11.
