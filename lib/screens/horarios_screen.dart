import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';
import '../services/api_service.dart';

class HorariosManagementScreen extends StatefulWidget {
  const HorariosManagementScreen({super.key});

  @override
  State<HorariosManagementScreen> createState() =>
      _HorariosManagementScreenState();
}

class _HorariosManagementScreenState extends State<HorariosManagementScreen> {
  final _apiService = ApiService();
  List<dynamic> _horarios = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadHorarios();
  }

  void _loadHorarios() async {
    setState(() => _isLoading = true);
    final list = await _apiService.getListaHorarios();
    setState(() {
      _horarios = list;
      _isLoading = false;
    });
  }

  void _abrirFormulario({Map<String, dynamic>? horario}) async {
    final turnoController = TextEditingController(text: horario?['turno']);
    final inicioController = TextEditingController(text: horario?['inicio']);
    final finController = TextEditingController(text: horario?['fin']);

    // Días de la semana
    List<String> diasSeleccionados =
        horario?['dias'] != null && horario!['dias'] != "No definido"
        ? horario['dias'].toString().split(',')
        : [];

    final todosDias = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"];

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          backgroundColor: const Color(0xFF1E293B),
          title: Text(horario == null ? "Nuevo Horario" : "Editar Horario"),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  controller: turnoController,
                  decoration: const InputDecoration(
                    labelText: "Nombre Turno (ej. Mañana)",
                  ),
                ),
                const SizedBox(height: 10),
                Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: inicioController,
                        decoration: const InputDecoration(
                          labelText: "Inicio (HH:MM)",
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: TextField(
                        controller: finController,
                        decoration: const InputDecoration(
                          labelText: "Fin (HH:MM)",
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                const Text(
                  "Días Laborales:",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                Wrap(
                  spacing: 5,
                  children: todosDias.map((dia) {
                    final isSelected = diasSeleccionados.contains(dia);
                    return FilterChip(
                      label: Text(dia),
                      selected: isSelected,
                      onSelected: (val) {
                        setDialogState(() {
                          if (val)
                            diasSeleccionados.add(dia);
                          else
                            diasSeleccionados.remove(dia);
                        });
                      },
                      selectedColor: const Color(0xFFD4AF37),
                    );
                  }).toList(),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("CANCELAR"),
            ),
            ElevatedButton(
              onPressed: () async {
                final datos = {
                  'turno': turnoController.text,
                  'inicio': inicioController.text,
                  'fin': finController.text,
                  'dias': diasSeleccionados.join(','),
                };
                if (horario == null) {
                  await _apiService.crearHorario(datos);
                } else {
                  await _apiService.editarHorario(horario['id'], datos);
                }
                Navigator.pop(context);
                _loadHorarios();
              },
              child: const Text("GUARDAR"),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("GESTIÓN DE HORARIOS")),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _abrirFormulario(),
        child: const Icon(Icons.add),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(10),
              itemCount: _horarios.length,
              itemBuilder: (context, index) {
                final h = _horarios[index];
                return FadeInRight(
                  delay: Duration(milliseconds: index * 100),
                  child: Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(
                        Icons.access_time,
                        color: Color(0xFFD4AF37),
                      ),
                      title: Text(h['turno']),
                      subtitle: Text(
                        "${h['inicio']} - ${h['fin']}\nDías: ${h['dias']}",
                      ),
                      trailing: IconButton(
                        icon: const Icon(Icons.edit, color: Colors.blue),
                        onPressed: () => _abrirFormulario(horario: h),
                      ),
                    ),
                  ),
                );
              },
            ),
    );
  }
}
