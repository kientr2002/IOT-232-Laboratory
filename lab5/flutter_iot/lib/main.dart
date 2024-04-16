import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('IOT Lab 5'),
        ),
        body: MyHomePage(),
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  MqttServerClient? client;
  bool PumpClick = false;
  bool LEDClick = false;
  String temperature = '34';
  String humidity = '45';

  @override
  void publishLedState(int state) {
    final builder = MqttClientPayloadBuilder();
    builder.addString('$state');
    client!.publishMessage(
      'kientranvictory/feeds/button1',
      MqttQos.atLeastOnce,
      builder.payload!,
    );
  }

  void publishPumpState(int state) {
    final builder = MqttClientPayloadBuilder();
    builder.addString('$state');
    client!.publishMessage(
      'kientranvictory/feeds/button2',
      MqttQos.atLeastOnce,
      builder.payload!,
    );
  }

  void initState() {
    super.initState();
    connectToMqtt();
  }

  void connectToMqtt() async {
    client = MqttServerClient('io.adafruit.com', 'kientranvictory');
    client!.logging(on: true);
    client!.onConnected = onConnected;
    client!.onDisconnected = onDisconnected;
    client!.onSubscribed = onSubscribed;

    final mqttConnectMessage = MqttConnectMessage()
        .withClientIdentifier('clientId')
        .startClean()
        .keepAliveFor(60)
        .withWillTopic('willtopic')
        .withWillMessage('Will message')
        .withWillQos(MqttQos.atLeastOnce);
    client!.connectionMessage = mqttConnectMessage;

    try {
      await client!.connect('kientranvictory', ''); // Dien Password vao day
    } catch (e) {
      print('MQTT: Exception: $e');
      client!.disconnect();
    }
  }

  void onConnected() {
    print('MQTT: Connected');
    client!.subscribe('kientranvictory/feeds/sensor1', MqttQos.atMostOnce);
    client!.subscribe('kientranvictory/feeds/sensor2', MqttQos.atMostOnce);
    client!.subscribe('kientranvictory/feeds/button1', MqttQos.atMostOnce);
    client!.subscribe('kientranvictory/feeds/button2', MqttQos.atMostOnce);
    client!.updates?.listen((List<MqttReceivedMessage<MqttMessage>>? c) {
      final MqttPublishMessage recMess = c![0].payload as MqttPublishMessage;
      final pt =
          MqttPublishPayload.bytesToStringAsString(recMess.payload.message!);
      String feed = c[0].topic;
      if (feed == 'kientranvictory/feeds/sensor1') {
        setState(() {
          temperature = pt;
        });
        print('MQTT: feed $feed has received data from server: $pt°C');
      } else if (feed == 'kientranvictory/feeds/sensor2') {
        setState(() {
          humidity = pt;
        });
        print('MQTT: feed $feed has received data from server: $pt%');
      } else if (feed == 'kientranvictory/feeds/button1') {
        setState(() {
          LEDClick = (pt == '0' ? false : true);
        });
        print('MQTT: feed $feed has received data from server: $pt');
      } else if (feed == 'kientranvictory/feeds/button2') {
        setState(() {
          PumpClick = (pt == '0' ? false : true);
        });
        print('MQTT: feed $feed has received data from server: $pt');
      }
    });
  }

  void onDisconnected() {
    print('MQTT: Disconnected');
  }

  void onSubscribed(String topic) {
    print('MQTT: Subscribed to topic $topic');
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        Expanded(
          flex: 1,
          child: Row(
            children: [
              Expanded(
                flex: 1,
                child: Image(
                  image: AssetImage('assets/logo.jpg'),
                ),
              ),
              Expanded(
                flex: 9,
                child: Container(
                  child: Center(
                    child: Text(
                      'Tran Van Kien - 2013552',
                      style: TextStyle(
                        fontSize: 25,
                        color: Colors.green,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        Expanded(
          flex: 4,
          child: Row(
            children: [
              Expanded(
                flex: 1,
                child: Padding(
                  padding: EdgeInsets.all(15),
                  child: Container(
                    color: Colors.red,
                    child: Center(
                      child: Text(
                        '$temperature°C',
                        style: TextStyle(
                          fontSize: 25,
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              Expanded(
                flex: 1,
                child: Padding(
                  padding: EdgeInsets.all(15),
                  child: Container(
                    color: Colors.blue,
                    child: Center(
                      child: Text(
                        '$humidity%',
                        style: TextStyle(
                          fontSize: 25,
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        Expanded(
          flex: 2,
          child: Padding(
            padding: EdgeInsets.all(15),
            child: SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () {
                  setState(() {
                    PumpClick = !PumpClick;
                  });
                  int pumpState = PumpClick ? 1 : 0;
                  publishPumpState(pumpState);
                },
                icon: Icon(Icons.power_settings_new),
                label: Text('PUMP'),
                style: ElevatedButton.styleFrom(
                  backgroundColor:
                      (PumpClick == true) ? Colors.yellow : Colors.white,
                ),
              ),
            ),
          ),
        ),
        Expanded(
          flex: 2,
          child: Padding(
            padding: EdgeInsets.all(15),
            child: SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () {
                  setState(() {
                    LEDClick = !LEDClick;
                  });
                  int ledState = LEDClick ? 1 : 0;
                  publishLedState(ledState);
                },
                icon: Icon(Icons.lightbulb_outline),
                label: Text('LED'),
                style: ElevatedButton.styleFrom(
                  backgroundColor:
                      (LEDClick == true) ? Colors.yellow : Colors.white,
                ),
              ),
            ),
          ),
        ),
        Expanded(
          flex: 1,
          child: Container(
            color: Colors.white,
          ),
        ),
      ],
    );
  }

  @override
  void dispose() {
    client?.disconnect();
    super.dispose();
  }
}
