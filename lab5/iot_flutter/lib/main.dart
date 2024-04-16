import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Flexible Vertical Split'),
        ),
        body: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Expanded(
              flex: 1,
              child: Row(
                children: [
                  Expanded(
                    flex: 1,
                    child: Container(
                       child: Icon(Icons.info),
                    ),
                  ),
                  Expanded(
                    flex: 9,
                    child: Container(
                      child: Center(child: Text('Tran Van Kien - 2013552')),
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
                    child: Container(
                      color: Colors.green,
                      child: Center(child: Text('2')),
                    ),
                  ),
                  Expanded(
                    flex: 1,
                    child: Container(
                      color: Colors.green,
                      child: Center(child: Text('4')),
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              flex: 2,
              child: Container(
                color: Colors.yellow,
                child: Center(child: Text('3')),
              ),
            ),
            Expanded(
              flex: 2,
              child: Container(
                color: const Color.fromARGB(255, 68, 65, 33),
                child: Center(child: Text('3')),
              ),
            ),
            Expanded(
              flex: 1,
              child: Container(
                color: Colors.red,
                child: Center(child: Text('5')),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
