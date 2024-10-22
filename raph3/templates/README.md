This is a small web application that runs asynchronously on the device and allows you to configure your IoT or OT project in a user-friendly way.

Since the front end is not my particular fascination, you can see that it is really simple but functional.

TECHNICAL DETAILS

- The idea of ​​this website is that through javascript, the data of the devices on the network is obtained through an http query to "/api/ping" to each IP in the local network where the device is streaming.

To reduce the workload, these "scans" are performed by the personal device with which you connect to the IP of the IoT device, be it a notebook, cell phone, tablet, etc. (NOTE: I thought of this this way to avoid saturating the network when there are many devices on the network, this way only the device that acts as "broker" performs said scan occasionally.

The time of all the devices on the network is also synchronized after obtaining the list of devices through the url "/api/timestamp" using the javascript function "syncDevicesTime() line 142 of raph.js

The list of devices on the raph3 network is sent to said devices in the syncNetwork() function of the raph.js javascript line 179

The page is updated every 5 seconds by default, printing the device statuses on the interface, you can configure it as you like, especially if you are going to use a computer on the network to save that information. You can do it in raph.js on line 12 (setInterval(updateDevices, ActionTimeInMilliseconds))

Once the desired actions are loaded into the device, it works without the need for a broker or device using the application, it is only a method to configure them in a simple way. Keep in mind that you are free to create and use the one you want within your project, just remember that you must make the corresponding modifications in /raph3/raph.py within startup_routes() if you use different file names or other technologies.