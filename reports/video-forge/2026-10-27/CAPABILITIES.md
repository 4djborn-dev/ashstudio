# CAPABILITIES — аудит окружения видеостудии

Дата: 2026-10-27T14:22:49+05:00 (Asia/Yekaterinburg).
Рабочая папка: `C:\Users\ASUS PC\OneDrive\Рабочий стол\Навыки режессуры`.

Аудит выполнен по части 1 VIDEO-FORGE.md.markdown с адаптацией Linux/macOS-команд к Windows. Установок, обновлений и удаления существующих файлов не было. Синтетическая проверка энкодеров не является производством ролика. Команды, коды возврата и фактический вывод приведены ниже. YES для find_spec/списка FFmpeg означает обнаружение, а не полноценную проверку выполнения. NO в поиске исполняемого файла означает отсутствие в явно проверенных местах, не доказательство отсутствия на всех дисках.


## Таблица возможностей

| Раздел | Возможность | Статус | Доказательство (команда + вывод) | Влияние на видео |
|---|---|---|---|---|
| 1 | ОС, CPU, память, диск | YES | [E001](#e001) | Снимок свободных ресурсов на момент аудита; скорость рендера этим не измерена. |
| 1 | Python и архитектура процесса | YES | [E002](#e002) | Определяет локальный runtime. |
| 2 | Видеоадаптеры и драйверы Windows | YES | [E003](#e003) | AdapterRAM из WMI может быть ограничен 32 битами; это не достоверный объём VRAM для больших GPU. |
| 2 | nvidia-smi | NO | [E004](#e004) | CUDA и NVENC не подтверждены этой проверкой. |
| 2 | VAAPI / VideoToolbox | NOT_APPLICABLE | [E005](#e005) | Linux VAAPI и macOS VideoToolbox не являются backend этой Windows-машины. |
| 3 | FFmpeg, используемый текущими скриптами студии | YES | [E006](#e006) | Текущий assemble.py использует этот бинарник; он может отличаться от полной сборки. |
| 3 | Версия и конфигурация | YES | [E007](#e007) | Регистрация backend/опций не доказывает их работоспособность на GPU. |
| 3 | Backend аппаратного ускорения | YES | [E008](#e008) | Регистрация backend/опций не доказывает их работоспособность на GPU. |
| 3 | Пути ffmpeg / ffprobe | YES | [E009](#e009) | Для запуска нужны абсолютные пути, если бинарники отсутствуют в PATH. |
| 3 | Энкодер h264_nvenc | YES | [E010](#e010) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер hevc_nvenc | YES | [E011](#e011) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер av1_nvenc | YES | [E012](#e012) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер h264_qsv | YES | [E013](#e013) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер hevc_qsv | YES | [E014](#e014) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер h264_amf | YES | [E015](#e015) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер hevc_amf | YES | [E016](#e016) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер h264_vaapi | YES | [E017](#e017) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер h264_videotoolbox | NO | [E018](#e018) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер libx264 | YES | [E019](#e019) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер libx265 | YES | [E020](#e020) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер libvpx | YES | [E021](#e021) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер libvpx-vp9 | YES | [E022](#e022) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер libaom-av1 | YES | [E023](#e023) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Энкодер libsvtav1 | YES | [E024](#e024) | Наличие в сборке; аппаратный запуск проверяется отдельно. |
| 3 | Фильтр zoompan | YES | [E025](#e025) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр xfade | YES | [E026](#e026) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр overlay | YES | [E027](#e027) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр drawtext | YES | [E028](#e028) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр subtitles | YES | [E029](#e029) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр ass | YES | [E030](#e030) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр eq | YES | [E031](#e031) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр curves | YES | [E032](#e032) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр lut3d | YES | [E033](#e033) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр colorbalance | YES | [E034](#e034) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр vidstabdetect | YES | [E035](#e035) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр vidstabtransform | YES | [E036](#e036) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр minterpolate | YES | [E037](#e037) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр unsharp | YES | [E038](#e038) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр blend | YES | [E039](#e039) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр alphamerge | YES | [E040](#e040) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр amix | YES | [E041](#e041) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр adelay | YES | [E042](#e042) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр afade | YES | [E043](#e043) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр loudnorm | YES | [E044](#e044) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр sidechaincompress | YES | [E045](#e045) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр apad | YES | [E046](#e046) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Фильтр concat | YES | [E047](#e047) | Доступность указанной операции в сборке FFmpeg. |
| 3 | Декодер hevc | YES | [E048](#e048) | Проверка реальных файлов ниже; список декодеров не равен успешному чтению файла. |
| 3 | Декодер av1 | YES | [E049](#e049) | Проверка реальных файлов ниже; список декодеров не равен успешному чтению файла. |
| 3 | Декодер prores | YES | [E050](#e050) | Проверка реальных файлов ниже; список декодеров не равен успешному чтению файла. |
| 3 | Практический запуск libx264 | YES | [E051](#e051) | Проверка работы энкодера, без установки и без сохранения медиа. |
| 3 | Практический запуск h264_nvenc | NO | [E052](#e052) | Проверка работы энкодера, без установки и без сохранения медиа. |
| 3 | Практический запуск h264_qsv | NO | [E053](#e053) | Проверка работы энкодера, без установки и без сохранения медиа. |
| 3 | Практический запуск h264_amf | YES | [E054](#e054) | Проверка работы энкодера, без установки и без сохранения медиа. |
| 3 | Проверка кодеков существующих видео | YES | [E103](#e103) | Метаданные доступных файлов; весь глубокий архив не сканировался. |
| 3 | Реальное декодирование hevc | NOT_TESTED | [E104](#e104) | Наличие декодера подтверждено отдельно; практическое чтение не подтверждено. |
| 3 | Реальное декодирование av1 | NOT_TESTED | [E105](#e105) | Наличие декодера подтверждено отдельно; практическое чтение не подтверждено. |
| 3 | Реальное декодирование prores | NOT_TESTED | [E106](#e106) | Наличие декодера подтверждено отдельно; практическое чтение не подтверждено. |
| 4 | Python version / pip inventory | YES | [E055](#e055) | Установленные пакеты в используемом Python; импорт каждого отдельно не гарантирован. |
| 4 | pillow | YES | [E056](#e056) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | numpy | YES | [E057](#e057) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | opencv | NO | [E058](#e058) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | moviepy | NO | [E059](#e059) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | imageio | YES | [E060](#e060) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | imageio_ffmpeg | YES | [E061](#e061) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | av | YES | [E062](#e062) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | matplotlib | NO | [E063](#e063) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | cairo | NO | [E064](#e064) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | cairosvg | NO | [E065](#e065) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | manim | NO | [E066](#e066) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | skia | NO | [E067](#e067) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | scipy | YES | [E068](#e068) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | scikit-image | YES | [E069](#e069) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | librosa | NO | [E070](#e070) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | soundfile | YES | [E071](#e071) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | pydub | NO | [E072](#e072) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | Coqui TTS | NO | [E073](#e073) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | piper | NO | [E074](#e074) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | pyttsx3 | NO | [E075](#e075) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | edge_tts | NO | [E076](#e076) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | faster-whisper | YES | [E077](#e077) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | fonttools | NO | [E078](#e078) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 4 | sounddevice | NO | [E079](#e079) | Проверено наличие модуля; работоспособность и модели не проверены этим вызовом. |
| 5 | Node | YES | [E080](#e080) | Версия / наличие Node-инструментов. |
| 5 | npm | YES | [E081](#e081) | Версия / наличие Node-инструментов. |
| 5 | npm global packages | YES | [E082](#e082) | Версия / наличие Node-инструментов. |
| 5 | Рабочий проект Remotion | YES | [E083](#e083) | Состав проекта и зависимости из manifest. |
| 5 | Remotion: вызов --version (неподдержанный флаг) | NO | [E084](#e084) | Версия 4.0.538 выведена самой CLI; exit=1 относится к синтаксису вызова. Успешная команда versions приведена отдельно. |
| 5 | Chrome / Chromium / Edge | YES | [E085](#e085) | Наличие браузера не равнозначно проверенному рендеру Remotion. |
| 5 | Remotion: фактические версии пакетов | YES | [E109](#e109) | Команда versions работает. --version в E084 вернула справку и exit=1: это неподдержанный способ запроса версии, а не отсутствие Remotion. Headless-рендер NOT_TESTED; ничего не скачивалось. |
| 6 | Blender | NO | [E086](#e086) | Headless/Cycles/render time: NOT_TESTED, Blender не обнаружен. Не утверждается отсутствие в произвольных папках. |
| 7 | espeak | NO | [E087](#e087) | Проверено обнаружение команды в PATH, не вся файловая система. |
| 7 | espeak-ng | NO | [E088](#e088) | Проверено обнаружение команды в PATH, не вся файловая система. |
| 7 | festival | NO | [E089](#e089) | Проверено обнаружение команды в PATH, не вся файловая система. |
| 7 | piper | NO | [E090](#e090) | Проверено обнаружение команды в PATH, не вся файловая система. |
| 7 | say | NO | [E091](#e091) | Проверено обнаружение команды в PATH, не вся файловая система. |
| 7 | sox | NO | [E092](#e092) | Проверено обнаружение команды в PATH, не вся файловая система. |
| 7 | SAPI voices Windows | YES | [E093](#e093) | Список голосов SAPI; синтез речи и качество не проверены. Language 419 обозначает ru-RU. |
| 7 | Аудиоустройства Windows | YES | [E094](#e094) | Это список контроллеров, не доказательство доступности микрофона для записи. |
| 7 | Активные capture endpoints (микрофоны) | YES | [E095](#e095) | DeviceState=1 означает active endpoint; фактическая запись и разрешения приложений NOT_TESTED. |
| 8 | Покрытие шрифтов | NOT_TESTED | [E096](#e096) | Нельзя подтвердить кириллицу по одному имени файла. |
| 8 | Шрифты: проверка средствами Windows | YES | [E107](#e107) | Проверены глифы русского алфавита через GDI; первые 20 семейств. Для китайского проверены только 中文. DejaVu/Noto/Liberation не найдены среди установленных семейств; есть Arial и другие варианты с кириллицей. |
| 8 | Явный путь к шрифту Arial | YES | [E108](#e108) | Можно задавать абсолютный fontfile для титров с кириллицей; визуальный тест титра не выполнялся. |
| 9 | https://pypi.org | YES | [E097](#e097) | Доступ к индексу сейчас; загрузка пакетов не выполнялась. |
| 9 | https://registry.npmjs.org | YES | [E098](#e098) | Доступ к индексу сейчас; загрузка пакетов не выполнялась. |
| 9 | Права записи в проект | YES | [E099](#e099) | Подтверждение записи только в папку проекта. |
| 9 | Администратор / sudo | NO | [E100](#e100) | Права администратора не повышались; возможность установки без них не проверялась. |
| 10 | Корень проекта | YES | [E101](#e101) | Инвентаризация без изменения существующих активов. |
| 10 | Медиа до глубины 3 папок | YES | [E102](#e102) | Вложенные материалы сцен могут лежать глубже и не входят в этот ограниченный список. |

## Вердикт по четырём вопросам

**Q1. Может ли машина собрать видео из готовых кадров? — Да, базовые средства подтверждены.** FFmpeg 9.0.2, ffprobe, libx264, zoompan, xfade, overlay, drawtext/ASS, concat и звуковые фильтры обнаружены. libx264 и AMD h264_amf успешно закодировали по 12 синтетических кадров 320×180. В существующих файлах ffprobe прочитал H.264, размеры, fps и длительности. Есть шрифты с кириллицей. Полный новый ролик с монтажом, титрами и звуком в рамках аудита не производился; время такого рендера NOT_TESTED.

**Q2. Может ли генерировать движение/анимацию кодом? — Да для FFmpeg; Remotion установлен, рендер не проверен.** Нужные фильтры FFmpeg перечислены отдельно. Команда Remotion versions подтвердила 4.0.538 и согласованность пакетов. Chrome и Edge обнаружены, однако headless-рендер Remotion NOT_TESTED. Manim не обнаружен в используемом Python. Нельзя выдавать наличие пакетов за успешный рендер.

**Q3. Может ли рендерить 3D-сцену? — Не подтверждено.** Blender не найден в PATH и в стандартной папке Blender Foundation. Blender headless, Cycles, CUDA/OPTIX/METAL и время кадра NOT_TESTED по этой причине. Наличие AMD Vega 8 само по себе не доказывает поддержку конкретного режима Cycles. Время 3D-рендера не оценивалось.

**Q4. Чего не хватает для полного цикла сценарий → видео?** Для локальной сборки из предоставленных кадров/клипов обязательных недостающих установок по этому аудиту не выявлено. Русский голос Microsoft Irina Desktop зарегистрирован в Windows SAPI, поэтому утверждать отсутствие всей локальной TTS нельзя; синтез WAV и качество речи NOT_TESTED. faster-whisper найден, но импорт, наличие весов и распознавание NOT_TESTED. Seedance и внешние генераторы не входили в аудит локального окружения; по правилам текущего проекта их запускает пользователь.

Порядок дальнейших действий / условных установок:

1. **P0 — без установки:** использовать полные абсолютные пути к FFmpeg/ffprobe. Важно: существующий assemble.py обращается к imageio_ffmpeg с FFmpeg 7.1, а полный набор возможностей в этой справке проверен на отдельном FFmpeg 9.0.2. Нельзя автоматически переносить результаты проверки одной сборки на другую.
2. **P1 — проверка без установки:** выполнить небольшой Remotion-рендер с явно выбранным уже установленным браузером; отдельно проверить SAPI-синтез и Whisper с имеющимися моделями. Если модели отсутствуют, их загрузку планировать отдельно. Это необходимые дополнительные доказательства только для обещаний соответствующих функций.
3. **P2 — условная установка Blender:** нужна только если в объём студии входит процедурный 3D-превиз. После установки потребуются headless-проверка и измерение реального времени кадра; сейчас этих данных нет.
4. **P3 — условная установка Manim:** нужна только для специализированных математических/диаграммных анимаций. OpenCV, MoviePy, matplotlib, Cairo/CairoSVG, skia, librosa и pydub отсутствуют в проверенном Python, но их отсутствие не блокирует монтаж через FFmpeg. Не устанавливать весь список без конкретной задачи.

По классификации вложения: **уровень B с оговорками** для локального производства из имеющихся активов. Наличие всех художественных исходников конкретного заказа, качество озвучки, полный рендер Remotion и 3D не подтверждены. Сроки производства не измерены и не обещаются.

## Ограничения измерений

- Ресурсы памяти и диска — снимок во время аудита. В E001 свободно 727228 KiB RAM при 6237464 KiB видимой RAM; свободно 36445167616 байт на C:. Значения не являются постоянными характеристиками доступности ресурсов.
- NVENC и Quick Sync зарегистрированы в сборке, но их практические вызовы завершились ошибкой. AMD AMF H.264 прошёл практический запуск. Скорость и качество энкодеров не сравнивались.
- HEVC, AV1 и ProRes есть в списке декодеров; реальное чтение этих кодеков NOT_TESTED: в проверенной выборке до 20 видео не найден подходящий тестовый файл.
- Проверка шрифтов через fontTools не выполнена из-за отсутствия пакета; вместо неё выполнена проверка средствами Windows GDI (E107). Визуальная читабельность титра отдельно не оценивалась.
- Пакеты проверены через find_spec в C:\Python314\python.exe; возможные другие Python/venv не инвентаризировались. Наличие пакета не гарантирует успешный импорт/исполнение.
- Поиск инструментов ограничен PATH и указанными стандартными папками. Сеть проверена HEAD-запросами, без установки пакетов. Права администратора не повышались. Запись микрофона не выполнялась.
- Инвентарь медиа ограничен корнем и тремя уровнями подпапок, в список включены первые 30 совпадений. Глубокие папки сцен не проверялись целиком.


## Проверки проекта и побочные изменения

Создан файл `CAPABILITIES.md`. Обязательный `selftest.py` пересобрал существующий служебный файл `Ролики/Драка-у-бара/Сцена-1-до-удара/4-Промпты/_служебное/refs.lock.json` через `build_prompt.py`. Это побочное изменение обязательной проверки; исходный слепок содержит хэш, а не резервную копию содержимого, поэтому точное восстановление исходных байтов не выполнялось. Guard сообщил WARN о CRLF этого служебного файла. Принятые изображения и поля visual_check не менялись. Новых изображений нет, кропы не создавались. Код студии не исправлялся в этой задаче.

Selftest: exit=0, 26/26. Guard: exit=0, автоматический итог OK; оставшийся WARN приведён в полном выводе ниже.

Команда:
```text
python film-directing-core/studio/selftest.py "Ролики/Драка-у-бара/Сцена-1-до-удара/Паспорт-сцены.yaml"
```

Полный вывод отдельного запуска selftest:
```text
PASS selftest дыра в шкале: validator дал FAIL
PASS selftest отсутствующий файл: validator дал FAIL
PASS selftest два location: validator дал FAIL
PASS selftest нет identity у HERO: validator дал FAIL
PASS selftest последний план с hard_cut: validator дал FAIL
PASS selftest дыра в beats: validator дал FAIL
PASS selftest инвариант без check: validator дал FAIL
PASS selftest неверный аспект keyframe: validator дал FAIL
PASS selftest one-door ограничен по shots: validator дал FAIL
PASS selftest референс изменён после сборки: validator дал FAIL
PASS selftest visual_check image4=pending: FAIL
PASS selftest visual_check image1=pending: WARN only
PASS selftest per-shot cut warning
PASS selftest takes missing: validator WARN/PASS, assemble ERROR
PASS selftest approve_ref сложные notes и перенос строки
PASS selftest исходный паспорт: validator дал PASS
PASS selftest общий промпт: 8 референсов без отбора дают FAIL по лимиту
PASS selftest общий промпт: 6 отобранных референсов, теги в пределах @image1…6
PASS selftest общий промпт: general_refs на 6 проходят validator
PASS selftest промпты: интервалы абзацев в 4 файлах
PASS selftest промпт 4 плана: EXACTLY THREE CUTS
PASS selftest detector cuts: expected [15, 30], got [15, 30]
PASS selftest assembly: duration 10.0s, cuts [2.0, 4.0]
ИТОГО: 23/23 проверок пройдено
PASS selftest assemble_film synthetic: duration 12.130s, fps 23.990; PASS разбор: C:\Users\ASUS PC\AppData\Local\Temp\_film_selftest_h9mhg1ur\Разбор-2026-10-27
Длительность 12.130 с; склейки: 0.500, 1.000, 1.125
PASS selftest assemble_film errors: отсутствует final и неизвестный type
PASS selftest кодировка: ошибок нет
ИТОГО: 26/26 проверок пройдено
```

Команда:
```text
python film-directing-core/studio/codex_guard.py check
```

Полный вывод check:
```text
Задача: Аудит окружения VIDEO-FORGE; отчёт CAPABILITIES.md  (слепок 2026-10-27T14:17:55)
Изменено: 1, новых: 1, удалено: 0
  ~ Ролики/Драка-у-бара/Сцена-1-до-удара/4-Промпты/_служебное/refs.lock.json
  + CAPABILITIES.md
selftest Ролики/Драка-у-бара/Сцена-1-до-удара/Паспорт-сцены.yaml: OK

WARN Ролики/Драка-у-бара/Сцена-1-до-удара/4-Промпты/_служебное/refs.lock.json: переводы строк CRLF (нужен newline="\n")

ИТОГ: OK по автоматике

В отчёте режиссёру обязательно:
  1. Какие файлы созданы/изменены (список выше) и зачем.
  2. Что проверено кропами и что увидено в каждом спорном месте.
  3. Сомнения и нарушения инвариантов — прямо, без «всё чисто» без проверки.
  4. Что осталось FAIL/WARN и почему.
  visual_check не ставь — приёмку делает режиссёр.
```

## Доказательства

### E001

Команда / метод:
```text
$os=Get-CimInstance Win32_OperatingSystem; $cpu=Get-CimInstance Win32_Processor; $d=Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"; [pscustomobject]@{OS=$os.Caption;Version=$os.Version;Build=$os.BuildNumber;Architecture=$os.OSArchitecture;CPU=($cpu.Name -join '; ');LogicalProcessors=($cpu.NumberOfLogicalProcessors | Measure-Object -Sum).Sum;RAMTotalKiB=$os.TotalVisibleMemorySize;RAMFreeKiB=$os.FreePhysicalMemory;DiskTotalBytes=$d.Size;DiskFreeBytes=$d.FreeSpace} | ConvertTo-Json
```

Фактический вывод:
```text
exit=0
{
    "OS":  "Microsoft Windows 11 Home",
    "Version":  "10.0.26200",
    "Build":  "26200",
    "Architecture":  "64-bit",
    "CPU":  "AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx  ",
    "LogicalProcessors":  8,
    "RAMTotalKiB":  6237464,
    "RAMFreeKiB":  727228,
    "DiskTotalBytes":  254772842496,
    "DiskFreeBytes":  36445167616
}
```

### E002

Команда / метод:
```text
sys.executable; platform.platform(); platform.machine(); os.cpu_count()
```

Фактический вывод:
```text
C:\Python314\python.exe
Windows-11-10.0.26200-SP0
AMD64
logical CPUs=8
```

### E003

Команда / метод:
```text
Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM,DriverVersion,VideoProcessor,Status | ConvertTo-Json
```

Фактический вывод:
```text
exit=0
{
    "Name":  "AMD Radeon(TM) Vega 8 Graphics",
    "AdapterRAM":  2147483648,
    "DriverVersion":  "27.20.11044.7",
    "VideoProcessor":  "AMD Radeon Graphics Processor (0x15D8)",
    "Status":  "OK"
}
```

### E004

Команда / метод:
```text
shutil.which + System32/NVSMI paths
```

Фактический вывод:
```text
NOT_FOUND; executable lookup, no process exit code
```

### E005

Команда / метод:
```text
platform.system()
```

Фактический вывод:
```text
Windows
```

### E006

Команда / метод:
```text
imageio_ffmpeg.get_ffmpeg_exe()
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe
```

### E007

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -version
```

Фактический вывод:
```text
exit=0
ffmpeg version 9.0.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers
built with gcc 16.2.0 (Rev3, Built by MSYS2 project)
configuration: --enable-gpl --enable-version3 --enable-static --disable-w32threads --disable-autodetect --enable-cairo --enable-fontconfig --enable-iconv --enable-gnutls --enable-lcms2 --enable-libxml2 --enable-gmp --enable-bzlib --enable-lzma --enable-libsnappy --enable-zlib --enable-librist --enable-libsrt --enable-libssh --enable-libzmq --enable-avisynth --enable-libbluray --enable-libcaca --enable-libdvdnav --enable-libdvdread --enable-sdl2 --enable-libaribb24 --enable-libaribcaption --enable-libdav1d --enable-libdavs2 --enable-libopenjpeg --enable-libquirc --enable-libuavs3d --enable-libxevd --enable-libzvbi --enable-liboapv --enable-libqrencode --enable-librav1e --enable-libsvtav1 --enable-libvvenc --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxavs2 --enable-libxeve --enable-libxvid --enable-libaom --enable-libjxl --enable-libsvtjpegxs --enable-libvpx --enable-mediafoundation --enable-libass --enable-frei0r --enable-libfreetype --enable-libfribidi --enable-libharfbuzz --enable-liblensfun --enable-libvidstab --enable-libvmaf --enable-libzimg --enable-amf --enable-cuda-llvm --enable-cuvid --enable-dxva2 --enable-d3d11va --enable-d3d12va --enable-ffnvcodec --enable-libvpl --enable-nvdec --enable-nvenc --enable-vaapi --enable-vulkan --enable-libplacebo --enable-opencl --enable-libcdio --enable-openal --enable-libgme --enable-libmodplug --enable-libopenmpt --enable-libopencore-amrwb --enable-libmp3lame --enable-libshine --enable-libtheora --enable-libtwolame --enable-libvo-amrwbenc --enable-libcodec2 --enable-libilbc --enable-libgsm --enable-liblc3 --enable-libopencore-amrnb --enable-libopus --enable-libspeex --enable-libvorbis --enable-ladspa --enable-libbs2b --enable-libflite --enable-libmysofa --enable-librubberband --enable-libsoxr --enable-chromaprint --enable-whisper
libavutil      61.  1.102 / 61.  1.102
libavcodec     63.  1.102 / 63.  1.102
libavformat    63.  1.102 / 63.  1.102
libavdevice    63.  1.102 / 63.  1.102
libavfilter    12.  1.102 / 12.  1.102
libswscale     10.  1.102 / 10.  1.102
libswresample   7.  1.102 /  7.  1.102

Exiting with exit code 0
```

### E008

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -hwaccels
```

Фактический вывод:
```text
exit=0
Hardware acceleration methods:
cuda
vaapi
dxva2
qsv
d3d11va
opencl
vulkan
d3d12va
amf
```

### E009

Команда / метод:
```text
shutil.which + WinGet lookup
```

Фактический вывод:
```text
PATH ffmpeg=None
PATH ffprobe=None
Selected ffmpeg=C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe
Selected ffprobe=C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffprobe.exe
ffprobe exists=True
```

### E010

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: h264_nvenc]
```

Фактический вывод:
```text
V....D h264_nvenc           NVIDIA NVENC H.264 encoder (codec h264)
```

### E011

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: hevc_nvenc]
```

Фактический вывод:
```text
V....D hevc_nvenc           NVIDIA NVENC hevc encoder (codec hevc)
```

### E012

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: av1_nvenc]
```

Фактический вывод:
```text
V....D av1_nvenc            NVIDIA NVENC av1 encoder (codec av1)
```

### E013

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: h264_qsv]
```

Фактический вывод:
```text
V..... h264_qsv             H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (Intel Quick Sync Video acceleration) (codec h264)
```

### E014

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: hevc_qsv]
```

Фактический вывод:
```text
V..... hevc_qsv             HEVC (Intel Quick Sync Video acceleration) (codec hevc)
```

### E015

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: h264_amf]
```

Фактический вывод:
```text
V....D h264_amf             AMD AMF H.264 Encoder (codec h264)
```

### E016

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: hevc_amf]
```

Фактический вывод:
```text
V....D hevc_amf             AMD AMF HEVC encoder (codec hevc)
```

### E017

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: h264_vaapi]
```

Фактический вывод:
```text
V....D h264_vaapi           H.264/AVC (VAAPI) (codec h264)
```

### E018

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: h264_videotoolbox]
```

Фактический вывод:
```text
NOT_LISTED (parent command exit=0)
```

### E019

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: libx264]
```

Фактический вывод:
```text
V....D libx264              libx264 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (codec h264)
```

### E020

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: libx265]
```

Фактический вывод:
```text
V....D libx265              libx265 H.265 / HEVC (codec hevc)
```

### E021

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: libvpx]
```

Фактический вывод:
```text
V....D libvpx               libvpx VP8 (codec vp8)
```

### E022

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: libvpx-vp9]
```

Фактический вывод:
```text
V....D libvpx-vp9           libvpx VP9 (codec vp9)
```

### E023

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: libaom-av1]
```

Фактический вывод:
```text
V....D libaom-av1           libaom AV1 (codec av1)
```

### E024

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -encoders [filter exact name: libsvtav1]
```

Фактический вывод:
```text
V..... libsvtav1            SVT-AV1(Scalable Video Technology for AV1) encoder (codec av1)
```

### E025

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: zoompan]
```

Фактический вывод:
```text
.. zoompan           V->V       Apply Zoom & Pan effect.
```

### E026

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: xfade]
```

Фактический вывод:
```text
.S xfade             VV->V      Cross fade one video with another video.
```

### E027

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: overlay]
```

Фактический вывод:
```text
TS overlay           VV->V      Overlay a video source on top of the input.
```

### E028

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: drawtext]
```

Фактический вывод:
```text
T. drawtext          V->V       Draw text on top of video frames using libfreetype library.
```

### E029

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: subtitles]
```

Фактический вывод:
```text
.. subtitles         V->V       Render text subtitles onto input video using the libass library.
```

### E030

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: ass]
```

Фактический вывод:
```text
.. ass               V->V       Render ASS subtitles onto input video using the libass library.
```

### E031

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: eq]
```

Фактический вывод:
```text
T. eq                V->V       Adjust brightness, contrast, gamma, and saturation.
```

### E032

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: curves]
```

Фактический вывод:
```text
TS curves            V->V       Adjust components curves.
```

### E033

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: lut3d]
```

Фактический вывод:
```text
TS lut3d             V->V       Adjust colors using a 3D LUT.
```

### E034

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: colorbalance]
```

Фактический вывод:
```text
TS colorbalance      V->V       Adjust the color balance.
```

### E035

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: vidstabdetect]
```

Фактический вывод:
```text
.. vidstabdetect     V->V       Extract relative transformations, pass 1 of 2 for stabilization (see vidstabtransform for pass 2).
```

### E036

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: vidstabtransform]
```

Фактический вывод:
```text
.. vidstabtransform  V->V       Transform the frames, pass 2 of 2 for stabilization (see vidstabdetect for pass 1).
```

### E037

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: minterpolate]
```

Фактический вывод:
```text
.. minterpolate      V->V       Frame rate conversion using Motion Interpolation.
```

### E038

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: unsharp]
```

Фактический вывод:
```text
TS unsharp           V->V       Sharpen or blur the input video.
```

### E039

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: blend]
```

Фактический вывод:
```text
TS blend             VV->V      Blend two video frames into each other.
```

### E040

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: alphamerge]
```

Фактический вывод:
```text
T. alphamerge        VV->V      Copy the luma value of the second input into the alpha channel of the first input.
```

### E041

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: amix]
```

Фактический вывод:
```text
.. amix              N->A       Audio mixing.
```

### E042

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: adelay]
```

Фактический вывод:
```text
T. adelay            A->A       Delay one or more audio channels.
```

### E043

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: afade]
```

Фактический вывод:
```text
T. afade             A->A       Fade in/out input audio.
```

### E044

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: loudnorm]
```

Фактический вывод:
```text
.. loudnorm          A->A       EBU R128 loudness normalization
```

### E045

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: sidechaincompress]
```

Фактический вывод:
```text
.. sidechaincompress AA->A      Sidechain compressor.
```

### E046

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: apad]
```

Фактический вывод:
```text
T. apad              A->A       Pad audio with silence.
```

### E047

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -filters [filter exact name: concat]
```

Фактический вывод:
```text
.. concat            N->N       Concatenate audio and video streams.
```

### E048

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -decoders [filter exact name: hevc]
```

Фактический вывод:
```text
VFS..D hevc                 HEVC (High Efficiency Video Coding)
```

### E049

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -decoders [filter exact name: av1]
```

Фактический вывод:
```text
V....D av1                  Alliance for Open Media AV1
```

### E050

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -decoders [filter exact name: prores]
```

Фактический вывод:
```text
VFS..D prores               Apple ProRes (iCodec Pro)
```

### E051

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -loglevel error -f lavfi -i testsrc2=size=320x180:rate=12 -frames:v 12 -c:v libx264 -f null -
```

Фактический вывод:
```text
exit=0
12 synthetic frames encoded
```

### E052

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -loglevel error -f lavfi -i testsrc2=size=320x180:rate=12 -frames:v 12 -c:v h264_nvenc -f null -
```

Фактический вывод:
```text
exit=4294967295
[h264_nvenc @ 0000019a76c1bdc0] Cannot load nvcuda.dll
[vost#0:0/h264_nvenc @ 0000019a76c1b340] [enc:h264_nvenc @ 0000019a76bee0c0] Error while opening encoder - maybe incorrect parameters such as bit_rate, rate, width or height.
[vf#0:0 @ 0000019a76c36c80] Error sending frames to consumers: Operation not permitted
[vf#0:0 @ 0000019a76c36c80] Task finished with error code: -1 (Operation not permitted)
[vf#0:0 @ 0000019a76c36c80] Terminating thread with return code -1 (Operation not permitted)
[vost#0:0/h264_nvenc @ 0000019a76c1b340] [enc:h264_nvenc @ 0000019a76bee0c0] Could not open encoder before EOF
[vost#0:0/h264_nvenc @ 0000019a76c1b340] Task finished with error code: -22 (Invalid argument)
[vost#0:0/h264_nvenc @ 0000019a76c1b340] Terminating thread with return code -22 (Invalid argument)
[out#0/null @ 0000019a76b6e740] Nothing was written into output file, because at least one of its streams received no packets.
```

### E053

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -loglevel error -f lavfi -i testsrc2=size=320x180:rate=12 -frames:v 12 -c:v h264_qsv -f null -
```

Фактический вывод:
```text
exit=2981409195
[h264_qsv @ 000002d02314bc00] Error creating a MFX session: -9.
[h264_qsv @ 000002d02314bc00] The current mfx implementation is not supported, try next mfx implementation.
[h264_qsv @ 000002d02314bc00] Error creating a MFX session: -9.
[vost#0:0/h264_qsv @ 000002d02314b180] [enc:h264_qsv @ 000002d023120880] Error while opening encoder - maybe incorrect parameters such as bit_rate, rate, width or height.
[vf#0:0 @ 000002d02314c840] Error sending frames to consumers: Unknown error occurred
[vf#0:0 @ 000002d02314c840] Task finished with error code: -1313558101 (Unknown error occurred)
[vf#0:0 @ 000002d02314c840] Terminating thread with return code -1313558101 (Unknown error occurred)
[vost#0:0/h264_qsv @ 000002d02314b180] [enc:h264_qsv @ 000002d023120880] Could not open encoder before EOF
[vost#0:0/h264_qsv @ 000002d02314b180] Task finished with error code: -22 (Invalid argument)
[vost#0:0/h264_qsv @ 000002d02314b180] Terminating thread with return code -22 (Invalid argument)
[out#0/null @ 000002d0230a0480] Nothing was written into output file, because at least one of its streams received no packets.
```

### E054

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -hide_banner -loglevel error -f lavfi -i testsrc2=size=320x180:rate=12 -frames:v 12 -c:v h264_amf -f null -
```

Фактический вывод:
```text
exit=0
12 synthetic frames encoded
```

### E055

Команда / метод:
```text
"C:\Python314\python.exe" -V; python -m pip list --format=json
```

Фактический вывод:
```text
Python 3.14.7 (tags/v3.14.7:823f032, Aug  5 2026, 10:51:32) [MSC v.1944 64 bit (AMD64)]
exit=0
installed packages=77
annotated-doc==0.0.5, annotated-types==0.8.0, anyio==4.15.1, attrs==26.1.0, av==19.0.2, certifi==2026.10.19, cffi==2.1.1, charset-normalizer==3.5.2, click==8.5.0, colorama==0.4.6, cryptography==50.0.2, ctranslate2==4.8.3, faster-whisper==1.2.1, filelock==4.2.4, flatbuffers==25.12.19, fsspec==2026.9.0, h11==0.16.0, hf-xet==1.7.0, httpcore==1.0.9, httpcore2==2.16.0, httpx==0.28.1, httpx-sse==0.4.3, httpx2==2.16.0, huggingface_hub==2.3.0, idna==3.20, ImageIO==2.38.1, imageio-ffmpeg==0.6.0, jsonschema==4.26.0, jsonschema-specifications==2025.9.1, lazy-loader==0.6, llvmlite==0.50.0, markdown-it-py==4.2.0, mcp==1.30.0, mdurl==0.1.2, networkx==3.7, numba==0.68.0, numpy==2.5.4, onnxruntime==1.31.0, packaging==26.3, pillow==13.0.0, pip==26.2.1, platformdirs==4.13.5, pooch==1.9.0, protobuf==7.36.2, pycparser==3.11, pydantic==2.14.1, pydantic_core==2.50.1, pydantic-settings==2.16.1, Pygments==2.21.0, PyJWT==2.15.1, pyloudnorm==0.2.0, PyMatting==1.1.16, python-dotenv==1.2.4, python-multipart==0.0.32, pywin32==312, PyYAML==6.0.3, referencing==0.37.0, rembg==2.0.86, requests==2.34.2, rich==15.0.0, rpds-py==2026.9.1, scikit-image==0.26.0, scipy==1.18.1, shellingham==1.5.4, soundfile==0.14.0, sse-starlette==3.5.0, starlette==1.9.0, tifffile==2026.10.15, tokenizers==0.23.3, tqdm==4.70.1, truststore==0.10.5, typer==0.27.3, typing_extensions==4.16.0, typing-inspection==0.4.4, urllib3==2.8.0, uvicorn==0.54.0, xdarkzx-reaper-mcp==0.8.3
```

### E056

Команда / метод:
```text
importlib.util.find_spec('PIL')
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\PIL\__init__.py
```

### E057

Команда / метод:
```text
importlib.util.find_spec('numpy')
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\numpy\__init__.py
```

### E058

Команда / метод:
```text
importlib.util.find_spec('cv2')
```

Фактический вывод:
```text
None
```

### E059

Команда / метод:
```text
importlib.util.find_spec('moviepy')
```

Фактический вывод:
```text
None
```

### E060

Команда / метод:
```text
importlib.util.find_spec('imageio')
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\imageio\__init__.py
```

### E061

Команда / метод:
```text
importlib.util.find_spec('imageio_ffmpeg')
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\__init__.py
```

### E062

Команда / метод:
```text
importlib.util.find_spec('av')
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\av\__init__.py
```

### E063

Команда / метод:
```text
importlib.util.find_spec('matplotlib')
```

Фактический вывод:
```text
None
```

### E064

Команда / метод:
```text
importlib.util.find_spec('cairo')
```

Фактический вывод:
```text
None
```

### E065

Команда / метод:
```text
importlib.util.find_spec('cairosvg')
```

Фактический вывод:
```text
None
```

### E066

Команда / метод:
```text
importlib.util.find_spec('manim')
```

Фактический вывод:
```text
None
```

### E067

Команда / метод:
```text
importlib.util.find_spec('skia')
```

Фактический вывод:
```text
None
```

### E068

Команда / метод:
```text
importlib.util.find_spec('scipy')
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\scipy\__init__.py
```

### E069

Команда / метод:
```text
importlib.util.find_spec('skimage')
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\skimage\__init__.py
```

### E070

Команда / метод:
```text
importlib.util.find_spec('librosa')
```

Фактический вывод:
```text
None
```

### E071

Команда / метод:
```text
importlib.util.find_spec('soundfile')
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\soundfile.py
```

### E072

Команда / метод:
```text
importlib.util.find_spec('pydub')
```

Фактический вывод:
```text
None
```

### E073

Команда / метод:
```text
importlib.util.find_spec('TTS')
```

Фактический вывод:
```text
None
```

### E074

Команда / метод:
```text
importlib.util.find_spec('piper')
```

Фактический вывод:
```text
None
```

### E075

Команда / метод:
```text
importlib.util.find_spec('pyttsx3')
```

Фактический вывод:
```text
None
```

### E076

Команда / метод:
```text
importlib.util.find_spec('edge_tts')
```

Фактический вывод:
```text
None
```

### E077

Команда / метод:
```text
importlib.util.find_spec('faster_whisper')
```

Фактический вывод:
```text
C:\Users\ASUS PC\AppData\Roaming\Python\Python314\site-packages\faster_whisper\__init__.py
```

### E078

Команда / метод:
```text
importlib.util.find_spec('fontTools')
```

Фактический вывод:
```text
None
```

### E079

Команда / метод:
```text
importlib.util.find_spec('sounddevice')
```

Фактический вывод:
```text
None
```

### E080

Команда / метод:
```text
node --version
```

Фактический вывод:
```text
exit=0
v24.19.0
```

### E081

Команда / метод:
```text
npm.cmd --version
```

Фактический вывод:
```text
exit=0
11.17.0
```

### E082

Команда / метод:
```text
npm.cmd list -g --depth=0
```

Фактический вывод:
```text
exit=0
C:\Users\ASUS PC\AppData\Roaming\npm
└── (empty)
```

### E083

Команда / метод:
```text
C:\Users\ASUS PC\Remotion
```

Фактический вывод:
```text
{
  "name": "remotion-studio",
  "version": "1.0.0",
  "private": true,
  "description": "Remotion workspace for vertical videos (used by Codex skill video-toolkit)",
  "scripts": {
    "studio": "remotion studio src/index.tsx",
    "render": "remotion render src/index.tsx",
    "still": "remotion still src/index.tsx",
    "compositions": "remotion compositions src/index.tsx"
  },
  "dependencies": {
    "@remotion/cli": "^4.0.538",
    "react": "^19.3.1",
    "react-dom": "^19.3.1",
    "remotion": "^4.0.538"
  }
}

```

### E084

Команда / метод:
```text
npx.cmd --no-install remotion --version; cwd=C:\Users\ASUS PC\Remotion
```

Фактический вывод:
```text
exit=1
@remotion/cli 4.0.538
© 2026 Remotion AG

Available commands:

remotion studio <entry-point>?
Start the Remotion Studio.
https://www.remotion.dev/docs/cli/studio

remotion render [<entry-point|serve-url>] [<composition-id>] [<output-location>]
Render video, audio or an image sequence.
https://www.remotion.dev/docs/cli/render

remotion still <serve-url|entry-point>? [<composition-id>] [<output-location>]
Render a still frame and save it as an image.
https://www.remotion.dev/docs/cli/still

remotion compositions <serve-url|entry-file>?
Print the available compositions.
https://www.remotion.dev/docs/cli/compositions

remotion lambda <command>
Control Remotion Lambda.
https://www.remotion.dev/docs/lambda/cli

remotion bundle <serve-url|entry-file>?
Create a Remotion bundle to be deployed to the web.
https://www.remotion.dev/docs/cli/bundle

remotion browser <command>
Ensure Remotion has a browser it can use for rendering.
https://www.remotion.dev/docs/cli/browser

remotion cloudrun <command>
Control Remotion Cloud Run.
https://www.remotion.dev/docs/cloudrun/cli

remotion benchmark [<entry-point>] [composition-ids]
Benchmark rendering one or more compositions.
https://www.remotion.dev/docs/cli/benchmark

remotion skills <add | update>
Install or update skills from remotion-dev/skills.
https://www.remotion.dev/docs/cli/skills

remotion versions
Print and validate versions of all Remotion packages.
https://www.remotion.dev/docs/cli/versions

remotion upgrade
Ensure Remotion is on the newest version.
https://www.remotion.dev/docs/cli/upgrade

remotion add <package-name...>
Add Remotion packages with the correct version.
https://www.remotion.dev/docs/cli/add

remotion gpu
Print information about how Chrome uses the GPU.
https://www.remotion.dev/docs/cli/gpu

remotion ffmpeg <arguments...>
Execute FFmpeg with all arguments forwarded.
https://www.remotion.dev/docs/cli/ffmpeg

remotion ffprobe <arguments...>
Execute FFprobe with all arguments forwarded.
https://www.remotion.dev/docs/cli/ffprobe

remotion help <command...>
Print available commands and flags for the Remotion CLI.
https://www.remotion.dev/docs/cli/help

Visit https://www.remotion.dev/docs/cli for browsable CLI documentation.
INTERPRETATION: --version returned CLI help, exit=1. Installed package version is confirmed by E109.
```

### E085

Команда / метод:
```text
Known Windows install paths + Remotion/Playwright/Puppeteer cache lookup
```

Фактический вывод:
```text
C:\Program Files\Google\Chrome\Application\chrome.exe
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

### E086

Команда / метод:
```text
shutil.which("blender"); C:/Program Files/Blender Foundation/Blender*/blender.exe
```

Фактический вывод:
```text
NOT_FOUND in checked paths; no process exit code
```

### E087

Команда / метод:
```text
shutil.which('espeak')
```

Фактический вывод:
```text
NOT_FOUND in PATH; no process exit code
```

### E088

Команда / метод:
```text
shutil.which('espeak-ng')
```

Фактический вывод:
```text
NOT_FOUND in PATH; no process exit code
```

### E089

Команда / метод:
```text
shutil.which('festival')
```

Фактический вывод:
```text
NOT_FOUND in PATH; no process exit code
```

### E090

Команда / метод:
```text
shutil.which('piper')
```

Фактический вывод:
```text
NOT_FOUND in PATH; no process exit code
```

### E091

Команда / метод:
```text
shutil.which('say')
```

Фактический вывод:
```text
NOT_FOUND in PATH; no process exit code
```

### E092

Команда / метод:
```text
shutil.which('sox')
```

Фактический вывод:
```text
NOT_FOUND in PATH; no process exit code
```

### E093

Команда / метод:
```text
$s=New-Object -ComObject SAPI.SpVoice; $s.GetVoices() | ForEach-Object { [pscustomobject]@{Name=$_.GetDescription();Language=$_.GetAttribute('Language');Id=$_.Id} } | ConvertTo-Json
```

Фактический вывод:
```text
exit=0
[
    {
        "Name":  "Microsoft Irina Desktop - Russian",
        "Language":  "419",
        "Id":  "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_RU-RU_IRINA_11.0"
    },
    {
        "Name":  "Microsoft Zira Desktop - English (United States)",
        "Language":  "409",
        "Id":  "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
    },
    {
        "Name":  "Microsoft David Desktop - English (United States)",
        "Language":  "409",
        "Id":  "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
    }
]
```

### E094

Команда / метод:
```text
Get-CimInstance Win32_SoundDevice | Select-Object Name,Manufacturer,Status | ConvertTo-Json
```

Фактический вывод:
```text
exit=0
[
    {
        "Name":  "AMD High Definition Audio Device",
        "Manufacturer":  "Advanced Micro Devices",
        "Status":  "OK"
    },
    {
        "Name":  "Realtek High Definition Audio",
        "Manufacturer":  "Realtek",
        "Status":  "OK"
    }
]
```

### E095

Команда / метод:
```text
Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Capture' | ForEach-Object { $v=Get-ItemProperty $_.PSPath; $p=Get-ItemProperty ($_.PSPath+'\Properties'); [pscustomobject]@{DeviceState=$v.DeviceState;Name=$p.'{a45c254e-df1c-4efd-8020-67d146a850e0},2';Description=$p.'{b3f8fa53-0004-438e-9003-51a46e139bfc},6'} } | ConvertTo-Json
```

Фактический вывод:
```text
exit=0
[
    {
        "DeviceState":  8,
        "Name":  "Microphone",
        "Description":  "Realtek(R) Audio"
    },
    {
        "DeviceState":  838860804,
        "Name":  "Internal AUX Jack",
        "Description":  "High Definition Audio Device"
    },
    {
        "DeviceState":  838860804,
        "Name":  "Internal AUX Jack",
        "Description":  "High Definition Audio Device"
    },
    {
        "DeviceState":  268435457,
        "Name":  "Stereo Mix",
        "Description":  "Realtek(R) Audio"
    },
    {
        "DeviceState":  570425348,
        "Name":  "Microphone",
        "Description":  "High Definition Audio Device"
    },
    {
        "DeviceState":  1,
        "Name":  "Microphone Array",
        "Description":  "Realtek(R) Audio"
    },
    {
        "DeviceState":  570425348,
        "Name":  "Microphone",
        "Description":  "High Definition Audio Device"
    },
    {
        "DeviceState":  822083588,
        "Name":  "Internal AUX Jack",
        "Description":  "AMD High Definition Audio Device"
    },
    {
        "DeviceState":  838860804,
        "Name":  "Internal AUX Jack",
        "Description":  "High Definition Audio Device"
    }
]
```

### E096

Команда / метод:
```text
fontTools font cmap scan
```

Фактический вывод:
```text
ModuleNotFoundError("No module named 'fontTools'")
```

### E097

Команда / метод:
```text
urllib.request.urlopen(HEAD, timeout=5): https://pypi.org
```

Фактический вывод:
```text
HTTP 200; elapsed=0.636s
```

### E098

Команда / метод:
```text
urllib.request.urlopen(HEAD, timeout=5): https://registry.npmjs.org
```

Фактический вывод:
```text
HTTP 200; elapsed=0.699s
```

### E099

Команда / метод:
```text
Write CAPABILITIES.md using Python open(encoding="utf-8", newline="\n")
```

Фактический вывод:
```text
Отчёт записан в корень проекта этим запуском (иначе процесс завершится ошибкой).
```

### E100

Команда / метод:
```text
ctypes.windll.shell32.IsUserAnAdmin()
```

Фактический вывод:
```text
False; sudo -n true: NOT_APPLICABLE (Windows)
```

### E101

Команда / метод:
```text
Path.cwd().iterdir()
```

Фактический вывод:
```text
DIR .keyframe-crops-8flw5jxh
DIR .v6-review-eo1udhr_
DIR _tmp_528wm8h_
FILE AGENTS.md
DIR codex-check-oavtln_l
DIR EffectCraft Auto-Save
DIR film-directing-core
DIR scene2-crops-114ia0hr
DIR tmp-s6-gkma5eyt
DIR tmprpxvafrb
DIR tmpwzkem0pp
DIR tmpxp2d10hl
FILE АСШ Студия — 3D логотип — слои.psd
FILE АСШ Студия — 3D логотип.ecproj
FILE АСШ Студия — 3D логотип.png
FILE АСШ Студия — 3D слои и анимация v02.ecproj
FILE АСШ Студия — 3D слои и анимация v02.mp4
FILE АСШ Студия — 3D слои и анимация v02.png
FILE АСШ Студия — 3D слои и анимация v02.psd
FILE АСШ Студия — независимые 3D-фейдеры v03.ecproj
FILE АСШ Студия — независимые 3D-фейдеры v03.mp4
FILE АСШ Студия — независимые 3D-фейдеры v03.png
DIR АСШ фейдеры SVG v03
FILE АСШ — 3D анимация слоёв.mp4
FILE Изображение ChatGPT 23 окт. 2026 г., 00_52_19.png
FILE Изображение ChatGPT 23 окт. 2026 г., 02_03_42.png
FILE Материалы_по_режиссуре_операторской_работе_и_монтажу.md
DIR Ролики
FILE Сцена 1
```

### E102

Команда / метод:
```text
os.walk: root + 3 directory levels; extension filter; first 30
```

Фактический вывод:
```text
Found=65
АСШ Студия — 3D логотип.png
АСШ Студия — 3D слои и анимация v02.mp4
АСШ Студия — 3D слои и анимация v02.png
АСШ Студия — независимые 3D-фейдеры v03.mp4
АСШ Студия — независимые 3D-фейдеры v03.png
АСШ — 3D анимация слоёв.mp4
Изображение ChatGPT 23 окт. 2026 г., 00_52_19.png
Изображение ChatGPT 23 окт. 2026 г., 02_03_42.png
film-directing-core\assets\08-раскадровка-драка-у-бара.png
film-directing-core\assets\10-раскадровка-pov-драки-графит.png
film-directing-core\assets\10-раскадровка-pov-драки.png
film-directing-core\assets\11-тест-continuity-board.png
film-directing-core\assets\12-раскадровка-графит-стиль-проход.png
film-directing-core\assets\13-пересобранная-раскадровка-драка-у-бара-layout.png
film-directing-core\assets\14-графитовая-раскадровка-драка-у-бара.png
film-directing-core\assets\16-графитовая-раскадровка-сцена-1-до-удара.png
film-directing-core\assets\18-графитовая-раскадровка-сцена-1-исправленная.png
film-directing-core\assets\19-карточка-персонажа-герой.jpeg
film-directing-core\assets\20-карточка-помещение-ракурсы-графит-концепт.png
film-directing-core\assets\20-раскадровка-сцена-1-по-карточкам-и-камере.png
film-directing-core\assets\21-окружение-бара-9x16-графит.png
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v1_draft.mp4
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v2_draft.mp4
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v3_draft.mp4
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v4_draft.mp4
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v4_draft_просмотр.mp4
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v5_draft.mp4
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v6_draft.mp4
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v7_master.mp4
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v7_просмотр.mp4
```

### E103

Команда / метод:
```text
"C:\Users\ASUS PC\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffprobe.exe" -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate:format=duration -of json <each>; max 20 shallow assets
```

Фактический вывод:
```text
АСШ Студия — 3D слои и анимация v02.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 1254,
            "height": 1254,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "6.400000"
    }
}
АСШ Студия — независимые 3D-фейдеры v03.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 1254,
            "height": 1254,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "6.400000"
    }
}
АСШ — 3D анимация слоёв.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 1254,
            "height": 1254,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "6.400000"
    }
}
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v1_draft.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 540,
            "height": 960,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "43.000000"
    }
}
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v2_draft.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 540,
            "height": 960,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "43.000000"
    }
}
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v3_draft.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 540,
            "height": 960,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "43.000000"
    }
}
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v4_draft.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 540,
            "height": 960,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "43.000000"
    }
}
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v4_draft_просмотр.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 540,
            "height": 960,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "43.000000"
    }
}
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v5_draft.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 540,
            "height": 960,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "43.000000"
    }
}
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v6_draft.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 540,
            "height": 960,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "43.008000"
    }
}
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v7_master.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 1080,
            "height": 1920,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "43.008000"
    }
}
Ролики\Воздушный-Шарм-открытия\Итоговый-ролик\VSh_43s_v7_просмотр.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 540,
            "height": 960,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "43.008000"
    }
}
Ролики\Драка-у-бара\Итоговый-ролик\Драка-у-бара-итог.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 1280,
            "height": 720,
            "r_frame_rate": "24/1"
        }
    ],
    "format": {
        "duration": "20.125000"
    }
}
Ролики\Милая-сниппет\Исходники\Milaya_animatic_9x16.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 1080,
            "height": 1920,
            "r_frame_rate": "30/1"
        }
    ],
    "format": {
        "duration": "51.100000"
    }
}
Ролики\Приглашение-на-юбилей\Монтаж\Черновик-v1.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 720,
            "height": 1280,
            "r_frame_rate": "24/1"
        }
    ],
    "format": {
        "duration": "38.250000"
    }
}
Ролики\Приглашение-на-юбилей\Монтаж\Черновик-v2.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 720,
            "height": 1280,
            "r_frame_rate": "24/1"
        }
    ],
    "format": {
        "duration": "38.250000"
    }
}
Ролики\Приглашение-на-юбилей\Монтаж\Черновик-v3-просмотр.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 720,
            "height": 1280,
            "r_frame_rate": "24/1"
        }
    ],
    "format": {
        "duration": "38.250000"
    }
}
Ролики\Приглашение-на-юбилей\Монтаж\Черновик-v3.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 720,
            "height": 1280,
            "r_frame_rate": "24/1"
        }
    ],
    "format": {
        "duration": "38.250000"
    }
}
Ролики\Приглашение-на-юбилей\Монтаж\Чистовой-1080.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 1080,
            "height": 1920,
            "r_frame_rate": "24/1"
        }
    ],
    "format": {
        "duration": "38.250000"
    }
}
Ролики\Приглашение-на-юбилей\Монтаж\Чистовой-720.mp4: exit=0; {
    "programs": [

    ],
    "stream_groups": [

    ],
    "streams": [
        {
            "codec_name": "h264",
            "width": 720,
            "height": 1280,
            "r_frame_rate": "24/1"
        }
    ],
    "format": {
        "duration": "38.250000"
    }
}
```

### E104

Команда / метод:
```text
Existing video inventory / ffprobe
```

Фактический вывод:
```text
Тестового файла с этим кодеком в проверенной выборке нет.
```

### E105

Команда / метод:
```text
Existing video inventory / ffprobe
```

Фактический вывод:
```text
Тестового файла с этим кодеком в проверенной выборке нет.
```

### E106

Команда / метод:
```text
Existing video inventory / ffprobe
```

Фактический вывод:
```text
Тестового файла с этим кодеком в проверенной выборке нет.
```

### E107

Команда / метод:
```text
System.Drawing InstalledFontCollection + Windows GDI CreateFontW/GetGlyphIndicesW(GGI_MARK_NONEXISTING_GLYPHS=1)
```

Фактический вывод:
```text
{
  "method": "System.Drawing InstalledFontCollection + Windows GDI CreateFontW/GetGlyphIndicesW(GGI_MARK_NONEXISTING_GLYPHS=1)",
  "family_count": 266,
  "russian_first_20": [
    "Arial",
    "Arial Black",
    "Arial Narrow",
    "Bahnschrift",
    "Bahnschrift Condensed",
    "Bahnschrift Light",
    "Bahnschrift Light Condensed",
    "Bahnschrift Light SemiCondensed",
    "Bahnschrift SemiBold",
    "Bahnschrift SemiBold Condensed",
    "Bahnschrift SemiBold SemiConden",
    "Bahnschrift SemiCondensed",
    "Bahnschrift SemiLight",
    "Bahnschrift SemiLight Condensed",
    "Bahnschrift SemiLight SemiConde",
    "Book Antiqua",
    "Bookman Old Style",
    "Bookshelf Symbol 7",
    "Calibri",
    "Calibri Light"
  ],
  "russian_matching_count": 132,
  "chinese_two_glyphs_first_5": [
    "Malgun Gothic",
    "Microsoft JhengHei",
    "Microsoft JhengHei Light",
    "Microsoft JhengHei UI",
    "Microsoft JhengHei UI Light"
  ],
  "named_families": {
    "DejaVu": [],
    "Noto": [],
    "Liberation": []
  }
}
```

### E108

Команда / метод:
```text
Path("C:/Windows/Fonts/arial.ttf").is_file()
```

Фактический вывод:
```text
True
```

### E109

Команда / метод:
```text
"C:\Users\ASUS PC\Remotion\node_modules\.bin\remotion.cmd" versions
```

Фактический вывод:
```text
exit=0
Node.JS = v24.19.0, OS = win32

On version: 4.0.538
- @remotion/bundler
- @remotion/sdk
- @remotion/cli
- @remotion/compositor-win32-x64-msvc
- remotion
- @remotion/licensing
- @remotion/media-utils
- @remotion/paths
- @remotion/player
- @remotion/renderer
- @remotion/streaming
- @remotion/codemods
- @remotion/studio-server
- @remotion/studio-shared
- @remotion/studio
- @remotion/timeline-utils
- @remotion/zod-types
- @remotion/captions
- @remotion/openai-whisper
- @remotion/elevenlabs
- @remotion/media
- @remotion/web-renderer
- @remotion/studio-protocol

Extra packages:
- zod@4.5.4

All packages have the correct version.
```

