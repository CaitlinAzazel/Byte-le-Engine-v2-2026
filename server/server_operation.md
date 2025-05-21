# Server Operation Manual

## Running the Server
For running the server, all the details are in `server_help_file.txt` and `server_readme.md`. Check those and you 
should have enough details!

NOTE: When you run the server and its terminals, *none of the terminals should be visible during the livestream*. Find 
a way to hide/isolate them from the viewers' perspective.

## Running OBS
1. Create a scene and name it "Screen" (or whatever you prefer)
2. Add a source to the scene. This will be a display capture
3. Specify which screen will be displayed from the display capture
   * It's best to select a screen instead of a window since the visualizer is only open temporarily
4. Set up your splash screen (a static image) if needed
    * This will be done by creating another source
    * This source can be called "Splash"
    * Find where this image is stored locally and set it from there
    * Ensure the source is a layer ***above*** the display capture source 
5. To keybind the splash screen:
   1. Go to _File → Settings → Hot Keys_
   2. Find "Screen"
   3. Find a pair called "Show 'Splash' Hide 'Splash'"
   4. Set the key binds from there

## Running Twitch
1. Log in to Twitch using the credentials in the Google Drive for board members
2. Get the Stream Key by:
   * Going to _Creator Dashboard → Settings → Stream_
   * Find the dropdown that says "Stream Key and Preferences"
   * Copy the primary Stream Key 
3. Put your Stream Key in OBS:
   1. Go to File → Settings → Stream
   2. Click "Use Stream Key"
   3. Paste your Stream Key
4. When you are ready to start the stream (splash screen is ready and terminals are live), click the button
to start the stream
