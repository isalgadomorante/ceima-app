# 🎓 Sistema de Gestión de Pagos — Secundaria y Bachillerato

## Instalación

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Acceso inicial
- **Usuario:** admin
- **Contraseña:** admin123

> Cambia la contraseña desde la base de datos SQLite después del primer acceso.

## Módulos incluidos

| Módulo | Descripción |
|--------|-------------|
| 📊 Dashboard | Métricas generales del mes y semáforo de alumnos |
| 👨‍🎓 Alumnos | Registro y catálogo de alumnos |
| 💳 Registrar Pago | Captura de pago con pronto pago automático y generación de recibo |
| 📋 Estado de Cuenta | Historial por alumno y semáforo de adeudos |
| 🔔 Recordatorios | Lista de alumnos a contactar con mensaje listo para WhatsApp |

## Lógica de pronto pago
- Pago registrado del **1 al 10 del mes** → 15% de descuento automático

## Semáforo de adeudos
- 🟢 **Al corriente** — pagos al día
- 🟡 **1 mes de adeudo** — seguimiento
- 🟡 **Llamar** — mes y medio de adeudo, llamar al tutor
- 🔴 **Restricción próxima** — 2.5 meses de adeudo

## Colegiaturas configuradas
- Secundaria: $3,780 / mes
- Bachillerato: $3,850 / mes
