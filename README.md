# 🚘 VialScore: Sistema de Incentivos Conductuales para el Transporte Público en el Perú

¡Bienvenido al repositorio oficial de **VialScore**! Un proyecto disruptivo desarrollado por el **Equipo NextStep** para el **AAP Innovation Challenge 2026** en conmemoración de los 100 años de la Asociación Automotriz del Perú.

> **Filosofía del Proyecto:** Porque cambiar el tránsito empieza por cambiar comportamientos, no solo por multar. 

---

## 🎯 El Problema Central vs Nuestra Solución
* **El Problema:** El transporte público en Lima genera pérdidas anuales de S/ 20,000 millones, velocidades promedio menores a 10 km/h y más de 3,000 muertes anuales debido a un sistema atomizado y una fiscalización puramente reactiva.
* **La Causa Raíz:** Los conductores no tienen incentivos positivos ni beneficios directos por cumplir las normas de tránsito.
* **La Solución (VialScore):** El primer sistema de **Crédito Social Conductual** en el Perú impulsado por Inteligencia Artificial y Monitoreo IoT. Evaluamos el estilo de conducción en tiempo real por viaje mediante variables telemétricas y premiamos el buen comportamiento convirtiéndolo en un activo económico directo para el conductor.

---

## 🛠️ Arquitectura de la Solución y Componentes del MVP
El proyecto consta de tres pilares integrados de software y hardware:
1. **Pilar 1 - Monitoreo Inteligente:** Procesamiento telemétrico mediante GPS, sensores de acelerómetros y cámaras con IA integradas en las unidades vehiculares.
2. **Pilar 2 - Score Dinámico (0-200 pts):** Algoritmo que calcula el desempeño por viaje clasificando a la flota en tres niveles: **Alto (150-200)**, **Medio (80-149)** y **Bajo (0-79)**.
3. **Pilar 3 - Beneficios Tangibles:** El puntaje se traduce directamente en descuentos en el SOAT, acceso a microcréditos viales, y subsidios de mantenimiento gracias a alianzas estratégicas corporativas y públicas.

---

## 💻 Tecnologías Utilizadas en este Repositorio
* **Python 3.10+** - Lenguaje base del core analítico y backend del negocio.
* **Streamlit** - Framework ágil enfocado en datos para desplegar el Panel Web de Operadores.
* **Plotly Express** - Generación de gráficos y analíticas dinámicas interactivos en tiempo Real.
* **Pandas** - Estructuración de datos y manejo de la matriz conductual de conductores.

---

## 🚀 Instrucciones de Instalación y Despliegue Local

Sigue estos pasos para clonar el repositorio y ejecutar el panel interactivo en tu entorno local:

1. **Clonar el repositorio:**
```bash
   git clone [https://github.com/tu-usuario/vialscore-nextstep.git](https://github.com/tu-usuario/vialscore-nextstep.git)
   cd vialscore-nextstep
