#!/usr/bin/env python3
"""
Script para probar los reportes mejorados del sistema de asistencia
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from system_optimized_v2 import OptimizedAttendanceSystem
from datetime import datetime, timedelta
import json

def test_reports():
    """Probar los reportes mejorados"""
    
    print("PRUEBA DE REPORTES MEJORADOS")
    print("=" * 50)
    
    # Inicializar sistema
    system = OptimizedAttendanceSystem()
    
    # Fechas de prueba (ultima semana)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    print(f"Generando reporte del {start_date} al {end_date}")
    
    # Probar reporte general
    print("\n1. REPORTE GENERAL:")
    report_data = system.generate_attendance_report(
        start_date.strftime('%Y-%m-%d'), 
        end_date.strftime('%Y-%m-%d')
    )
    
    if not report_data:
        print("No se generaron datos de reporte")
        return
    
    print(f"Empleados en reporte: {len(report_data)}")
    
    # Mostrar resumen por empleado
    for emp_id, emp_data in list(report_data.items())[:3]:  # Solo primeros 3
        print(f"\n{emp_data['name']} ({emp_data['department']}):")
        summary = emp_data['summary']
        print(f"   Dias trabajados: {summary['total_days_worked']}")
        print(f"   Horas totales: {summary['total_hours']}")
        print(f"   Promedio diario: {summary['average_daily_hours']}h")
        print(f"   Dias tarde: {summary['late_days']}")
        print(f"   Dias ausente: {summary['absent_days']}")
        
        # Mostrar algunos dias
        days_shown = 0
        for date_str, day_data in emp_data['days'].items():
            if days_shown >= 3:
                break
            if day_data['status'] != 'No laborable':
                print(f"   {day_data['date']}: {day_data['entrada'] or '--'} - {day_data['salida'] or '--'} ({day_data['hours_worked']}h) [{day_data['status']}]")
                if day_data['observations']:
                    print(f"      {', '.join(day_data['observations'])}")
                days_shown += 1
    
    # Probar reporte por departamento
    print(f"\n2. REPORTE POR DEPARTAMENTO (Reacondicionamiento):")
    dept_report = system.generate_attendance_report(
        start_date.strftime('%Y-%m-%d'), 
        end_date.strftime('%Y-%m-%d'),
        department='Reacondicionamiento'
    )
    
    print(f"Empleados de Reacondicionamiento: {len(dept_report)}")
    
    # Probar calculos de horas
    print(f"\n3. PRUEBA DE CALCULOS DE HORAS:")
    
    # Caso 1: Administrativo (10h - 1.33h breaks = 8.67h)
    hours1 = system.calculate_worked_hours("07:00:00", "17:00:00", "Reacondicionamiento")
    print(f"   Administrativo (7:00-17:00): {hours1}h (esperado: ~8.67h)")
    
    # Caso 2: Operativo (8h - 0.33h break = 7.67h)
    hours2 = system.calculate_worked_hours("06:00:00", "14:00:00", "Operativos")
    print(f"   Operativo (6:00-14:00): {hours2}h (esperado: ~7.67h)")
    
    # Caso 3: General (9h - 1.33h breaks = 7.67h)
    hours3 = system.calculate_worked_hours("08:00:00", "17:00:00", "General")
    print(f"   General (8:00-17:00): {hours3}h (esperado: ~7.67h)")
    
    # Probar dias laborales
    print(f"\n4. PRUEBA DE DIAS LABORALES:")
    
    test_date = datetime(2026, 1, 8)  # Miercoles
    weekend_date = datetime(2026, 1, 11)  # Sabado
    
    work_admin = system.is_work_day(test_date, 'administrativo', 'Reacondicionamiento')
    work_weekend = system.is_work_day(weekend_date, 'administrativo', 'Reacondicionamiento')
    work_operativo = system.is_work_day(weekend_date, 'turnos', 'Operativos')
    
    print(f"   Miercoles - Administrativo: {'Laboral' if work_admin else 'No laboral'}")
    print(f"   Sabado - Administrativo: {'Laboral' if work_weekend else 'No laboral'}")
    print(f"   Sabado - Operativo: {'Laboral' if work_operativo else 'No laboral'}")
    
    # Probar horarios por departamento
    print(f"\n5. PRUEBA DE HORARIOS POR DEPARTAMENTO:")
    
    horario_admin_lunes = system.get_expected_hours_by_department('Reacondicionamiento', 0)  # Lunes
    horario_admin_viernes = system.get_expected_hours_by_department('Reacondicionamiento', 4)  # Viernes
    horario_admin_sabado = system.get_expected_hours_by_department('Reacondicionamiento', 5)  # Sabado
    horario_operativo = system.get_expected_hours_by_department('Operativos', 0)  # Lunes
    
    print(f"   Reacondicionamiento - Lunes: {horario_admin_lunes}")
    print(f"   Reacondicionamiento - Viernes: {horario_admin_viernes}")
    print(f"   Reacondicionamiento - Sabado: {horario_admin_sabado}")
    print(f"   Operativos - Lunes: {horario_operativo}")
    
    print(f"\n6. ESTADISTICAS GENERALES:")
    
    total_employees = len(report_data)
    total_days_worked = sum(emp['summary']['total_days_worked'] for emp in report_data.values())
    total_hours = sum(emp['summary']['total_hours'] for emp in report_data.values())
    total_late_days = sum(emp['summary']['late_days'] for emp in report_data.values())
    
    print(f"   Total empleados: {total_employees}")
    print(f"   Total dias trabajados: {total_days_worked}")
    print(f"   Total horas trabajadas: {total_hours:.2f}")
    print(f"   Total dias con tardanza: {total_late_days}")
    
    if total_days_worked > 0:
        avg_hours_per_day = total_hours / total_days_worked
        print(f"   Promedio horas por dia: {avg_hours_per_day:.2f}")
    
    print(f"\n" + "=" * 50)
    print("PRUEBA DE REPORTES COMPLETADA")
    
    return report_data

if __name__ == "__main__":
    test_reports()