# VCamera

Manages a virtual camera camera device that transform the image captured from another camera (generally physical).
Uses `opencv` to read and transform images from the camera and the `v4l2-loopback` Linux kernel module to control the virtual camera.

## Setup and install

To install v4l2-loopback (in Debian and Ubuntu)
```
./install-v4l2.sh
```

To setup a virtual camera (unsing v4l2loopback module)
```
./setup-cameras.sh
```
or ten?
```
./setup-cameras.sh 10
```

## Running VCamera

To start a vcamera (assuming /dev/video0 is your capture device and /dev/video1 your virtual camera)
```
sudo ./vcamera.py -i /dev/video0 -o /dev/video1 -f flip sunset
```

To display the running vcamera at the browser start the webserver
```
./camera-select-app.py
```
or
```
./show-camera-app.py
```
and open the url [http://localhost:8080/](http://localhost:8080/).

## Customizing/Extending VCamera

The original image can be transformed by overriding the method `transform`
of class `VCamera` in a new subclass.

For fast development vcamera can be runned and displayed using opencv (`-p`)
```
sudo ./vcamera.py -i /dev/video0 -o /dev/video1 -f flip sunset -p
```

Some example filters to use at `transform` can be found at `filters.py`.
