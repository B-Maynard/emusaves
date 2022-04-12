# EmuSaves: A way to transfer save files for emulators from one directory to another (Best used with a cloud service)
*** Made in mind for the Steam Deck, haven't tested in other places ***

The main benefit of this script is to alleviate the copy/pasting between the cloud service provider and the local directory. I fought with getting cloud sync working on the Steam Deck for emulator files for the entire time I've had the device, but nothing seemed to work. I tried symlinking between the cloud folder and the save file folder, the games I tested wouldn't even boot this way. I tried just manually copy/pasting the files back and forth, this worked but was way too cumbersome. And not to mention, as far as I can tell, desktop services (like nextcloud) don't run in the background while in gaming mode anyway, so symlinking wouldn't matter unless you go back to the desktop mode and sync manually.

There's still quite a bit of manual setup but once that is done, its really simple to get your saves synced between devices (although its still not an automatic process)

In order to get full benefit out of the script:
- Get a cloud service provider set up locally with file system integration (I'm using the nextlcoud client with a folder setup in my documents to sync to, could do similar things with google drive I'd assume)

Once initial setup is done and you made your first config, startup your cloud service client, run this program, tell it how you want the files synced (either to the cloud service or from the cloud service), and done. The cloud service client will take care of the rest and your saves will now be all set in the cloud or on your local machine.

From here (on my main gaming tower running windows), I have a file that nextcloud syncs down to on that machine and I have symlinks setup and working there from the cloud folder to my local save folders. You could also do similar things with google drive here as well I'd assume. (Side note: not sure why the symlinks don't work in the same fashion on the steam deck as they do in windows, but I tried a bunch of different stuff with permissions and configuration and nothing seemed to ever work for the steam deck. the emulators would just freeze up and do nothing for me)
