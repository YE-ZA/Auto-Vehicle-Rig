# Auto-Vehicle-Rig

Auto Vehicle Rig is a tool to speed up the vehicle rigging process. 
The plugin supports 2-wheeled, 4-wheeled, and 6-wheeled vehicles. 
Users just need to click a few buttons to bind their custom vehicles.

the demo video link is here: https://vimeo.com/635027418

---

**Installation:** Copy the "scripts" and "prefs" folders to C:\Users\<Username>\Documents\maya\<version> folder.

Then open maya script editor and run the code below in a "python" tab:
```
from importlib import reload
import AutoVehicleRig.AVR_UI as ui
reload(ui)

AVRUI = ui.AVR()
```
