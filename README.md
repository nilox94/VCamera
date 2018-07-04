# VCamera

Manages a virtual camera by transforming the image captured from a real camera.
Uses opencv to read and transform images from the camera and v4l2-loopback
to control the virtual camera.

## Setup and install

To install v4l2-loopback
```
./install-v4l2.sh
```

To setup a virtual camera
```
./setup-cameras.sh
```
or ten?
```
./setup-cameras.sh 10
```

## Running VCamera

To start a vcamera
```
./vcamera.py
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

For fast development vcamera can be runned and displayed using opencv as in
```
./example.py
```

Some example filters to use at `transform` can be found at `filters.py`.