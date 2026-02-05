import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:animate_do/animate_do.dart';
import '../services/api_service.dart';

class AttendanceScreen extends StatefulWidget {
  const AttendanceScreen({super.key});

  @override
  State<AttendanceScreen> createState() => _AttendanceScreenState();
}

class _AttendanceScreenState extends State<AttendanceScreen> {
  final TextEditingController _dniController = TextEditingController();
  final ApiService _api = ApiService();
  bool _isLoading = false;

  void _processDni(String dni) async {
    if (dni.isEmpty) return;
    setState(() => _isLoading = true);

    final res = await _api.marcarAsistencia(dni);

    setState(() => _isLoading = false);
    _dniController.clear();
    if (res.containsKey('error')) {
      _showMsg(res['error'], Colors.redAccent);
    } else {
      _showSuccessDialog(
        res['mensaje'] ?? "Registro exitoso",
        res['empleado'] ?? "Empleado",
      );
    }
  }

  void _showMsg(String msg, Color color) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg),
        backgroundColor: color,
        behavior: SnackBarBehavior.floating,
        duration: const Duration(seconds: 4),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      ),
    );
  }

  void _showSuccessDialog(String msg, String emp) {
    showDialog(
      context: context,
      builder: (context) => ElasticIn(
        child: AlertDialog(
          backgroundColor: const Color(0xFF1E293B),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
            side: const BorderSide(color: Color(0xFFD4AF37), width: 2),
          ),
          title: const Icon(Icons.check_circle, color: Colors.green, size: 60),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                emp.toUpperCase(),
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                  color: Color(0xFFD4AF37),
                ),
              ),
              const SizedBox(height: 10),
              Text(
                msg,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 16),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text(
                "CERRAR",
                style: TextStyle(color: Color(0xFFD4AF37)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("REGISTRO DE JORNADA"),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.exit_to_app),
            onPressed: () => Navigator.pop(context),
          ),
        ],
      ),
      body: Container(
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF0F172A), Color(0xFF1E293B)],
          ),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(25),
          child: Column(
            children: [
              FadeInDown(
                child: const Text(
                  "ESCANEÉ SU CÓDIGO QR",
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2,
                    color: Color(0xFFD4AF37),
                  ),
                ),
              ),
              const SizedBox(height: 25),
              ZoomIn(
                child: Container(
                  height: 300,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(
                      color: const Color(0xFFD4AF37),
                      width: 3,
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: const Color(0xFFD4AF37).withOpacity(0.2),
                        blurRadius: 15,
                        spreadRadius: 2,
                      ),
                    ],
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(17),
                    child: MobileScanner(
                      onDetect: (capture) {
                        final List<Barcode> barcodes = capture.barcodes;
                        for (final barcode in barcodes) {
                          if (barcode.rawValue != null) {
                            _processDni(barcode.rawValue!);
                          }
                        }
                      },
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 40),
              FadeInUp(
                child: TextField(
                  controller: _dniController,
                  style: const TextStyle(color: Colors.white, fontSize: 18),
                  decoration: const InputDecoration(
                    hintText: "O INGRESE DNI MANUALMENTE",
                    prefixIcon: Icon(Icons.keyboard, color: Color(0xFFD4AF37)),
                  ),
                  keyboardType: TextInputType.number,
                  onSubmitted: _processDni,
                ),
              ),
              const SizedBox(height: 25),
              FadeInUp(
                delay: const Duration(milliseconds: 300),
                child: _isLoading
                    ? const CircularProgressIndicator(color: Color(0xFFD4AF37))
                    : ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          minimumSize: const Size(double.infinity, 60),
                          elevation: 10,
                        ),
                        onPressed: () => _processDni(_dniController.text),
                        child: const Text(
                          "REGISTRAR ASISTENCIA",
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
