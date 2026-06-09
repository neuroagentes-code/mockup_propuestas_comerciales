# Informe de Diagnóstico — Somos Circular

Gestora de residuos con modelo de economía circular ("el Airbnb de los residuos"). Operación Ara como piloto. 22 casos de uso. Capa de Validación Humana en cada decisión sensible.

### UC-01 — Prospectar leads y empresas objetivo por LinkedIn y buscadores

**Descripción**

Resuelve la prospección 100% manual de hoy. El agente identifica empresas grandes por sector (manufactura, alimentos, automotriz), encuentra los contactos de temas ambientales, envía mensajes personalizados y mantiene la conversación inicial hasta calificar el interés, usando como gancho la actualización normativa y la economía circular.

:::hitl
auto: Búsqueda de empresas y contactos, redacción y envío del mensaje inicial, seguimiento conversacional.
escala: El primer mensaje y el tono de prospección se aprueban una vez; los leads de alto valor se notifican al comercial antes de continuar.
notifica: Lead calificado y resumen de la conversación en la Plataforma; alerta al comercial.
:::

### UC-02 — Atender, calificar y agendar citas comerciales por WhatsApp, correo o teléfono

**Descripción**

Atiende el canal por donde hoy entra la mayoría de prospectos. El agente responde por WhatsApp, correo o teléfono, califica al prospecto con las variables clave que el comercial necesita —incluidas las condiciones del servicio—, agenda la cita y entrega un informe de prospección antes de la reunión.

:::hitl
auto: Atención conversacional, recolección de variables y condiciones, calificación, agendamiento de la cita, informe de prospección.
escala: El cierre de la negociación es atención humana; los casos de residuos peligrosos o ambiguos se marcan para revisión del comercial.
notifica: Cita agendada e informe de prospección en la Plataforma; alerta al comercial antes de la reunión por WhatsApp y correo.
:::

### UC-03 — Generar y publicar contenido de marketing con enfoque normativo y de economía circular

**Descripción**

Atiende la ausencia total de marketing estructurado. El agente genera contenido para redes (videos, carruseles, imágenes) con dos ganchos potentes: estar al día en normativa y el verdadero cierre de ciclo de la economía circular, para posicionar a Somos Circular como referente en un sector que hoy no lo tiene.

:::hitl
auto: Propuesta de temas, redacción de textos y guiones, preparación de piezas gráficas.
escala: Toda pieza queda en borrador hasta la aprobación del responsable de marketing antes de publicarse.
notifica: Contenido pendiente de aprobación en la Plataforma.
:::

### UC-04 — Construir el análisis financiero del cliente (modelo EBITDA) desde la reunión transcrita

**Descripción**

Automatiza el análisis que hoy se hace a mano en Excel. A partir de la reunión grabada y transcrita, el agente extrae las variables del cliente, corre el modelo financiero —prorrateando los costos administrativos generales de la empresa por proyecto— y entrega la utilidad bruta y el EBITDA aproximado, aplicando la regla de margen mínimo, para decidir si el cliente conviene y a qué precio ir.

:::hitl
auto: Extracción de variables desde la transcripción, consulta de la matriz de precios, prorrateo de costos administrativos, cálculo de margen y EBITDA con la regla de mínimo.
escala: El comercial revisa el resultado y puede ajustar variables antes de pasar a la propuesta; los casos fuera de regla se marcan.
notifica: Análisis corrido y disponible en la Plataforma para revisión del comercial.
:::

### UC-05 — Generar la propuesta comercial personalizada con aceptación por correo

**Descripción**

Convierte el análisis en la propuesta que hoy se arma semi-manual. El agente toma el Excel como insumo de precios y genera la propuesta personalizada desde una plantilla con los textos base editables, las tablas de valores y las condiciones, dejándola lista para enviarla y solicitar su aceptación por correo.

:::hitl
auto: Generación de la propuesta personalizada, inserción de tablas y condiciones, envío y solicitud de aceptación por correo.
escala: El comercial aprueba la propuesta antes de enviarla; la aceptación del cliente queda registrada por correo para evitar disputas.
notifica: Propuesta lista para envío y registro de aceptación en la Plataforma por correo.
:::

### UC-06 — Hacer seguimiento y recordatorios a las propuestas comerciales

**Descripción**

Atiende el seguimiento manual de hoy tras enviar una propuesta. El agente mantiene una secuencia de recordatorios al cliente para que ninguna propuesta enviada se enfríe ni se pierda por falta de seguimiento, y avisa al comercial del estado de cada una.

:::hitl
auto: Envío de recordatorios según cadencia, registro de respuestas, actualización del estado en el embudo.
escala: La negociación y las condiciones especiales las maneja el comercial; los silencios prolongados se escalan para decidir si se insiste o se cierra.
notifica: Estado del embudo y propuestas que requieren acción en la Plataforma por correo.
:::

### UC-07 — Gestionar la vinculación y la documentación bidireccional del cliente

**Descripción**

Atiende la creación de cliente que hoy se hace a mano. Al aceptar el cliente, el agente solicita por correo la documentación, crea automáticamente la carpeta del cliente, archiva lo que llega, registra los datos en la base única y mantiene la vigencia de cada documento, dejando solo la validación al responsable.

:::hitl
auto: Solicitud y recepción de documentos, creación de carpeta, archivado, registro en base de datos, verificación de vigencias y alertas.
escala: Administración valida la carpeta completa; los documentos faltantes o vencidos se escalan.
notifica: Estado de la carpeta y vigencias en la Plataforma; alerta por correo cuando falta o vence un documento.
:::

### UC-08 — Generar contratos y la declaración SAGRILAFT desde plantilla

**Descripción**

Estandariza los documentos legales que hoy se hacen caso por caso. El agente genera el contrato según el modelo que aplique (solo recolección, o con operación en planta) y la declaración juramentada de origen de recursos exigida por SAGRILAFT, a partir de los datos del cliente ya cargados.

:::hitl
auto: Selección del modelo, llenado de la plantilla de contrato y de la declaración SAGRILAFT.
escala: La firma del contrato y de la declaración la realiza el representante legal; cualquier cláusula fuera de plantilla se escala.
notifica: Documentos listos para firma en la Plataforma; alerta al representante legal.
:::

### UC-09 — Generar fichas técnicas y hojas de seguridad de residuos peligrosos como servicio

**Descripción**

Convierte una necesidad regulatoria en un servicio. Cada empresa debe tener las fichas técnicas y hojas de seguridad de los residuos peligrosos que genera; como no todas las tienen, el agente las genera con la información del residuo y la identidad del cliente, entregándolas como valor agregado que puede facturarse y que habilita el trámite ante el receptor.

:::hitl
auto: Generación de la ficha técnica y la hoja de seguridad con los datos del residuo y la identidad del cliente.
escala: El responsable ambiental revisa antes de entregar; los residuos sin información completa se marcan.
notifica: Documento listo para revisión y entrega en la Plataforma.
:::

### UC-10 — Programar y consolidar los cargues, asignar encargado y emitir la orden de recolección

**Descripción**

Automatiza el corazón operativo. El agente recibe la solicitud de cargue por WhatsApp o correo, pregunta y asegura todas las variables, llena el Excel de programación, la deja visible por día, asigna el encargado del cargue y emite la orden de recolección, confirmando el cargue tanto a las personas que van como a la empresa generadora.

:::hitl
auto: Recolección de variables, llenado del Excel, programación visible, asignación del encargado, generación y envío de la orden y de la confirmación.
escala: Los cargues urgentes fuera de política o con datos incompletos se escalan; la designación del encargado la confirma operaciones.
notifica: Programación visible por día, orden de recolección y confirmaciones en la Plataforma por WhatsApp y correo.
:::

### UC-11 — Conseguir flete y maquinaria, y hacer seguimiento de la llegada del cargue

**Descripción**

Resuelve el cuello de conseguir transporte y maquinaria —que hoy exige 3 o 4 llamadas— y el problema de los vehículos que llegan y esperan horas sin control. El agente difunde el cargue a los contactos del directorio, asigna al que confirma y, una vez en sitio, hace seguimiento por WhatsApp hasta confirmar la llegada y el inicio del cargue.

:::hitl
auto: Difusión del cargue, recepción de respuestas, asignación, registro del vehículo y maquinaria, recordatorios de llegada e inicio.
escala: La aprobación de la tarifa del flete o de la maquinaria, sobre todo en urgentes con sobrecosto, la valida operaciones.
notifica: Disponibilidad, asignación y estado de llegada del cargue en la Plataforma por WhatsApp.
:::

### UC-12 — Registrar la remisión digital, validar los pesos y verificar el material

**Descripción**

Digitaliza la remisión hoy física y blinda el dato del que depende toda la contabilidad y el margen. El encargado genera la remisión conversando con el agente o en un formulario; ambas partes la firman; y el agente valida que el peso y el tipo de material que salieron coincidan con lo que el receptor recibe, levantando alerta cuando hay merma sospechosa o degradación.

:::hitl
auto: Generación de la remisión, registro en base de datos, comparación de pesos y de tipo de material, detección de variaciones y degradación.
escala: La firma de la remisión la hacen siempre el encargado y el generador; toda variación fuera de umbral o cambio de material se escala para gestión con el cliente.
notifica: Remisión firmada, variaciones y alertas de material en la Plataforma por correo.
:::

### UC-13 — Tramitar la declaratoria y la documentación de residuos peligrosos (RESPEL) ante los receptores

**Descripción**

Atiende el trámite especializado de los peligrosos. Antes de entregar, el agente informa al receptor los residuos y cantidades (la declaratoria de residuos) y adjunta las hojas de seguridad; prepara el manifiesto de carga —que es la misma remisión que el conductor debe portar— y, según el receptor, tramita por correo o en su plataforma propia.

:::hitl
auto: Declaratoria por correo, preparación del manifiesto y de las hojas de seguridad, carga en receptores que operan por correo.
escala: La declaratoria en plataformas con credenciales y la confirmación del trámite las valida el responsable de calidad/ambiente.
notifica: Estado del trámite RESPEL por receptor en la Plataforma por correo.
:::

### UC-14 — Liquidar la facturación cruzada (compra de aprovechables y cobro de disposición)

**Descripción**

Resuelve el enredo del modelo cruzado: por los aprovechables, Somos Circular paga al cliente (compra el material); por los peligrosos y especiales, le cobra la disposición. Una vez validada la remisión, el agente calcula los netos y prepara los movimientos contables, entregándolos a la contadora con el régimen e impuestos.

:::hitl
auto: Cálculo de netos según naturaleza del residuo, preparación de los movimientos y de la solicitud a la contadora, informe de cierre de mes.
escala: La emisión y causación final las valida la contadora; cualquier diferencia con la remisión validada detiene la liquidación.
notifica: Movimientos preparados y pendientes de validación en la Plataforma por correo.
:::

### UC-15 — Conciliar bancos y cartera, calcular la utilidad y retener certificados por mora

**Descripción**

Cierra el ciclo financiero y convierte el cobro en proceso. El agente concilia el banco, calcula la utilidad bruta por cliente y ruta, gestiona la cartera y aplica la regla clave del negocio: el certificado (de impacto o de disposición) no se entrega al cliente hasta que el pago esté hecho.

:::hitl
auto: Conciliación de pagos y desembolsos, cálculo de utilidad, marcado de cartera, verificación de pago y retención del certificado.
escala: Las diferencias de conciliación y las gestiones de cobro las valida el responsable financiero.
notifica: Conciliación, cartera pendiente, utilidad por cliente/ruta y certificados retenidos en la Plataforma por correo.
:::

### UC-16 — Generar informes mensuales por centro de costos y por material

**Descripción**

Convierte los datos de la operación en los informes de gestión que hoy se arman a mano. El agente genera mensualmente los informes por centro de costos (por negocio o cliente) y por material, para que la dirección vea el desempeño sin tener que consolidarlo.

:::hitl
auto: Consolidación de datos y generación de los informes mensuales.
escala: La dirección revisa y aprueba los informes antes de su uso o difusión.
notifica: Informes mensuales disponibles en la Plataforma.
:::

### UC-17 — Generar certificados de disposición e informes de impacto ambiental

**Descripción**

Mejora, documenta y automatiza el certificado que ya diferencia a Somos Circular. Para los aprovechables, el agente genera el certificado de impacto automáticamente a cierre de mes; para los peligrosos y especiales, el certificado lo emite el tercero dispositor y el agente lo gestiona. En ambos casos, la entrega queda atada al pago.

:::hitl
auto: Cálculo de indicadores de impacto, generación y consecutivo del certificado de aprovechables, gestión del certificado del tercero, verificación de pago.
escala: El responsable ambiental aprueba el certificado de aprovechables antes de entregarlo; la liberación de cualquier certificado depende de la confirmación de pago.
notifica: Certificados emitidos, pendientes y retenidos por pago en la Plataforma por correo.
:::

### UC-18 — Generar los informes de cumplimiento ante la autoridad y monitorear los vencimientos normativos

**Descripción**

Ataca el verdadero cuello de botella: la burocracia ambiental. El agente monitorea los vencimientos y las fechas de los informes regulatorios —trimestrales y anuales—, prepara la documentación con la data interna y los certificados de los terceros, y apoya la radicación en la plataforma de la autoridad (ANLA), dejando la validación al Director HSEQ.

:::hitl
auto: Monitoreo de vencimientos y fechas, consolidación de data interna y certificados de terceros, preparación del trámite en la plataforma.
escala: El Director HSEQ valida y radica; los cambios normativos relevantes se escalan.
notifica: Alerta de vencimiento e informe listo para revisión en la Plataforma por correo.
:::

### UC-19 — Mantener un repositorio normativo vivo

**Descripción**

Crea el activo del que dependen el cumplimiento y el gancho de marketing. El agente mantiene una base viva de la normativa ambiental aplicable, detecta actualizaciones y las pone a disposición del equipo, convirtiendo "estar al día en normas" en una ventaja competitiva.

:::hitl
auto: Revisión de fuentes, detección de cambios, resumen y registro en el repositorio.
escala: La interpretación y el uso de un cambio normativo crítico se validan con el responsable ambiental.
notifica: Cambios normativos detectados notificados al equipo en la Plataforma.
:::

### UC-20 — Reclutar y filtrar candidatos con OCR y scoring

**Descripción**

Atiende el caos del reclutamiento, especialmente urgente ante la necesidad de contratar el personal de la operación Ara. El agente atiende el canal de vacantes, pide la documentación de forma conversacional, lee los adjuntos con visión artificial, actualiza la base y entrega un scoring con las mejores opciones.

:::hitl
auto: Atención del canal, solicitud y lectura de documentos por OCR, actualización de la base, scoring y recomendación.
escala: La decisión de contratación es siempre del reclutador; los perfiles ambiguos se marcan para revisión.
notifica: Candidatos evaluados y top de opciones en la Plataforma para el reclutador por WhatsApp y correo.
:::

### UC-21 — Capacitar y certificar empleados con un agente tutor

**Descripción**

Resuelve una exigencia legal —un operario no puede manipular residuos peligrosos sin capacitación previa— y protege a la empresa ante reclamaciones. El agente tutor da acceso restringido al módulo, despliega los temas obligatorios, evalúa, envía el resultado por correo y deja la trazabilidad para auditorías y defensa legal, sin parar la operación.

:::hitl
auto: Acceso, despliegue de módulos, evaluación, registro de trazabilidad, envío del resultado por correo con aceptación por silencio.
escala: La aprobación de contenidos y la validación de casos no aprobados las realiza el responsable de HSEQ.
notifica: Avance, certificación y reporte de cumplimiento por empleado en la Plataforma por correo.
:::

### UC-22 — Programar el mantenimiento preventivo y el rastreo de la maquinaria en planta

**Descripción**

Protege el CAPEX que la operación Ara exige (básculas, compactadoras y equipos). El agente registra cada máquina con su periodicidad de mantenimiento, programa los mantenimientos preventivos, genera reportes automáticos del estado y mantiene la trazabilidad, para pasar de mantenimientos correctivos a preventivos sin depender de una persona dedicada.

:::hitl
auto: Registro de máquinas y periodicidad, programación preventiva, convocatoria de aliados, reportes automáticos y registro de costos.
escala: La aprobación de los mantenimientos correctivos y de sus costos la valida operaciones.
notifica: Calendario de mantenimientos, pendientes y estado de la maquinaria en la Plataforma.
:::
