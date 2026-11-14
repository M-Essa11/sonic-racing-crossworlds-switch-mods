# CrossWorlds v2.00 Atmosphere patches

Both patches worked on my Switch Lite running Atmosphere. The FPS patch targets static 60 FPS. The resolution patch requests 100% render scale and targets 720p on handheld. Internal pixel dimensions and docked behavior have yet to be measured.

- Title ID `01006E001823C000`
- Build ID `D2B8094093CE27AE8C624765C054360F`

Extract the ZIP and merge its atmosphere folder into the SD card root. Disable any conflicting CrossWorlds FPS or graphics patches and fully restart the game.

```
atmosphere/exefs_patches/Sonic Racing CW v2.00 - Static 60FPS/D2B8094093CE27AE8C624765C054360F.ips
atmosphere/exefs_patches/Sonic Racing CW v2.00 - 720p Handheld Target/D2B8094093CE27AE8C624765C054360F.ips
```

Each patch can be installed or removed independently using its folder under atmosphere/exefs_patches. No FPSLocker configuration is required. Frame rate can vary by track.

All 39 patch writes and both IPS32 files passed static checks. The stable archive uses the exact patch bytes tested on Switch Lite. See validation.json for offsets, hashes and test scope.

Original FPS patch by [Fl4sh9174](https://github.com/Fl4sh9174/Switch-Emulator-Ultrawide-FPS-Mods). v2.00 port and Switch Lite testing by M-Essa11.
