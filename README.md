# Web Format Research Questionnaires

## Set up

Clone the repository to your preferred location:

```bash
cd your_directory
git clone https://github.com/nsnlab/questionnaires.git
```

## Run a questionnaire

### Option 1: Through the server with BIDS folder saving:

**Run python server scrip to open local server:**
```bash
cd /path/to/questionnaires   # Change this to your directory path
python server.py
```

**Navigate to webpage in browser:**
```
http://localhost:8000/
```

This opens a landing page with direct links to all currently available questionnaires.

**Submit a questionnaire and save data:**

After filling out a questionnaire, clicking "Submit" will trigger a save to the `data/` folder inside `/questionnaires`. The data will save in BIDS formatting: `sub-{subject}/{session}/beh/sub-{subject}_{session}_{time}_{questionnaire_type}.csv`

**Close server**

Press `Ctrl+C` in the terminal to stop the server.

### Option 2: Without server (data saves to Downloads folder)

**Open questionnaire directly:**

Navigate to the `html_web_forms/` folder in `/questionnaires`through the file browser of your computer and double click on the HTML file for the questionnaire of interest. This will open it directly in your default browser.

**Save data:**

After filling out a questionnaire, clicking "Submit" will trigger a download of the .csv output to the `/Downloads` folder of your computer. 

_**Note:**_ HTML questionnaire files can be directly shared to participants for remote completion using this method. They can be instructed to return the questionnaire by email, for example.

## Available Questionnaires

| Questionnaire | Editable PDF | Web Form | URL (with server.py active) |
|---------------|--------------|----------|----------|
| Leeds Sleep Scale | ✓ | ✓ | http://localhost:8000/leeds_sleep.html |
| Karolinska Sleepiness Scale (KSS) | ✓ | ✓ | http://localhost:8000/kss.html |
| Visual Analogue Mood Scale (VAMS) | ✓ | ✓ | http://localhost:8000/vams.html |
| TES Side Effects | ✓ | ✓ | http://localhost:8000/tes_side_effects.html |
| Sleep Diary | ✓ | ✓ | http://localhost:8000/sleep_diary.html |
| Munich Chronotype | ✓ | ✓ | http://localhost:8000/munich_chronotype.html |
| TACS/TIS Sensation Testing | | ✓ | http://localhost:8000/tacs_tis_sensation_testing.html |


_**Note:**_ The sleep diary questionnaire in web form has been adapted for single day entries.

## File Structure

```
questionnaires/
├── server.py              # Server script to open for BIDS saving
├── README.md              # This file
├── html_web_forms/        # HTML questionnaire files
│   ├── leeds_sleep.html
│   ├── kss.html
│   ├── vams.html
│   ├── tes_side_effects.html
│   ├── tacs_tis_sensation_testing.html
│   ├── sleep_diary.html
│   └── munich_chronotype.html
├── editable_PDFs/         # PDF format with entry fields
└── data/                  # Saved responses (auto-created)
```

## Data Output

When run through the server, form submissions are saved in compliance with BIDS to:
```
data/sub-{subject}/{session}/beh/
```

The `{identifier}` varies by questionnaire:
- **Pre/post questionnaires:** `{time}` (e.g., "pre-sleep", "post-sleep")
- **Region-based questionnaires:** `{region}` (e.g., "hippocampus", "DLPFC")

Otherwise, `.csv` files are downloaded to your computer's `/Downloads`

Each time a form is submitted, a new `.csv` file is created.

### Common Metadata Fields

All questionnaires include these standard fields:

| Field | Description |
|-------|-------------|
| `subject` | Subject ID (e.g., "001") |
| `experiment` | Experiment name (optional) |
| `session` | Session identifier (e.g., "ses-01") |
| `date` | Date of entry |
| `timestamp` | ISO 8601 timestamp of submission |

### Questionnaire-Specific Data Fields

#### Leeds Sleep Scale

| Field | Description |
|-------|-------------|
| `time` | Time of day (e.g., "pre-sleep", "post-sleep") |
| `gts_difficulty` | Getting to sleep: difficulty falling asleep (1-5) |
| `gts_speed` | Getting to sleep: speed of falling asleep (1-5) |
| `gts_sleepiness` | Getting to sleep: sleepiness rating (1-5) |
| `qos_restless` | Quality of sleep: restlessness (1-5) |
| `qos_wakeful` | Quality of sleep: wakefulness (1-5) |
| `afs_difficulty` | Awake from sleep: difficulty (1-5) |
| `afs_time` | Awake from sleep: time awake (minutes) |
| `bfw_wakeup` | Behavior following waking: how woke up (1-5) |
| `bfw_current` | Behavior following waking: current state (1-5) |
| `bfw_balance` | Behavior following waking: balance (1-5) |

**Filename format:** `sub-{subject}_{session}_{time}_leeds.csv`

#### Karolinska Sleepiness Scale (KSS)

| Field | Description |
|-------|-------------|
| `time` | Time of day (e.g., "pre-sleep", "post-sleep") |
| `KSS` | Sleepiness rating (1-10) |

**Filename format:** `sub-{subject}_{session}_{time}_kss.csv`

#### Visual Analogue Mood Scale (VAMS)

| Field | Description |
|-------|-------------|
| `time` | Time of day (e.g., "pre-sleep", "post-sleep") |
| `happy` | Happy rating (0-100) |
| `sad` | Sad rating (0-100) |
| `calm` | Calm rating (0-100) |
| `tense` | Tense rating (0-100) |
| `energetic` | Energetic rating (0-100) |
| `sleepy` | Sleepy rating (0-100) |

**Filename format:** `sub-{subject}_{session}_{time}_vams.csv`

#### TES Side Effects

| Field | Description |
|-------|-------------|
| `stim_count` | Number of stimulations before this session |
| `target_region` | Target brain region |
| `region_side` | Side (left/right/bilateral) |
| `tes_related` | Is this related to TES? |
| `{symptom}_present` | Symptom present? (yes/no) |
| `{symptom}_strength` | Symptom strength (slight/moderate/strong) |
| `{symptom}_onset` | Symptom onset (immediate/during/after) |
| `{symptom}_duration` | Symptom duration (seconds/minutes/hours) |
| `{symptom}_effect` | Effect on participant |
| `{symptom}_location` | Location on body |
| `{symptom}_electrode` | Near which electrode |
| `other_description` | Other symptom description |
| `stim_type` | Stimulation type |
| `intensity` | Stimulation intensity |
| `duration` | Stimulation duration |
| `impedance` | Electrode impedance |
| `electrode_setup` | Electrode setup type |
| `electrode_count` | Number of electrodes |
| `electrode_shape` | Electrode shape |
| `position_type` | Position type (coordinates/EEG cap) |
| `e{n}_{x/y/z}` | Electrode n coordinates |
| `e{n}_position` | Electrode n position |
| `adverse_events` | Adverse events notes |
| `investigator_comments` | Additional comments |
| `belief_sessions` | Belief sessions (semicolon-separated) |
| `belief_values` | Belief values (semicolon-separated) |

**Filename format:** `sub-{subject}_{session}_{region}_tes_side_effects.csv`

#### Sleep Diary

| Field | Description |
|-------|-------------|
| `time` | Time of day (pre-sleep/post-sleep) |
| `bedtime` | Time went to bed |
| `sleep_onset_latency` | Minutes to fall asleep |
| `awakenings` | Number of awakenings |
| `awake_time` | Total time awake (minutes) |
| `wake_time` | Final wake time |
| `rise_time` | Time got out of bed |
| `alarm_used` | Was alarm used? (yes/no) |
| `quality` | Sleep quality (1-5) |
| `refreshed` | How refreshed (1-5) |
| `caffeine` | Caffeine servings |
| `alcohol` | Alcohol servings |
| `napped` | Did you nap? (yes/no) |
| `nap_duration` | Nap duration (minutes) |
| `notes` | Additional notes |

**Filename format:** `sub-{subject}_{session}_{time}_sleep_diary.csv`

#### Munich Chronotype Questionnaire (MCTQ)

| Field | Description |
|-------|-------------|
| `regular_work` | Do you have regular work schedule? |
| `work_days` | Number of work days per week |
| `work_bedtime` | Work day bedtime |
| `work_sleep_ready` | Work day: ready to sleep time |
| `work_sleep_latency` | Work day: minutes to fall asleep |
| `work_wake_time` | Work day: wake time |
| `work_rise_latency` | Work day: minutes to get up |
| `work_alarm` | Work day: alarm used? |
| `work_alarm_before` | Work day: wake before alarm? |
| `free_bedtime` | Free day bedtime |
| `free_sleep_ready` | Free day: ready to sleep time |
| `free_sleep_latency` | Free day: minutes to fall asleep |
| `free_wake_time` | Free day: wake time |
| `free_rise_latency` | Free day: minutes to get up |
| `free_alarm` | Free day: alarm used? |
| `free_reasons` | Reasons for wake time |
| `free_reason_types` | Reason types |
| `free_reason_other` | Other reasons |

**Filename format:** `sub-{subject}_{session}_mctq.csv`

#### TACS/TIS Sensation Testing

**Multi-row format:** Each stimulation test creates a separate row. Both tACS and TIS support multiple tests via "Add another test" buttons.

| Field | Description |
|-------|-------------|
| `stim_count` | Number of stimulations before this session |
| `target_region` | Target brain region |
| `region_side` | Side (left/right/bilateral) |
| `test_type` | Type of test: `tacs` or `tis` |
| `test_number` | Test number (1, 2, 3, ...) |
| `frequency` | tACS frequency (Hz) — tACS only |
| `carrier_frequency` | TIS carrier frequency (Hz) — TIS only |
| `modulation_frequency` | TIS modulation frequency (Hz) — TIS only |
| `condition` | Perceived condition (real/placebo/dont_know) |
| `e12_threshold` | Electrodes 1-2 threshold (mA) |
| `e12_max_applied` | Electrodes 1-2 max applied (mA) |
| `e12_impedance` | Electrodes 1-2 impedance (kΩ) |
| `e12_sensations` | Electrodes 1-2 sensations (comma-separated) |
| `e12_location` | Electrodes 1-2 sensation location |
| `e12_other` | Electrodes 1-2 other sensation description |
| `e34_threshold` | Electrodes 3-4 threshold (mA) |
| `e34_max_applied` | Electrodes 3-4 max applied (mA) |
| `e34_impedance` | Electrodes 3-4 impedance (kΩ) |
| `e34_sensations` | Electrodes 3-4 sensations (comma-separated) |
| `e34_location` | Electrodes 3-4 sensation location |
| `e34_other` | Electrodes 3-4 other sensation description |
| `comments` | Additional comments |

**Sensation categories in `*_sensations` column:**
- **Discomfort:** Pain, Stinging, Pinching, Itching, Heat, Pinprick
- **Mechanical:** Tingling, Vibrations, Pushing, Pulling, Pressure
- **Reflex:** Pulse, Muscle spasm, Phosphenes, Hair prickle

**Filename format:** `sub-{subject}_{session}_{region}_tacs_tis_sensation.csv`

## Options

```bash
python server.py --port 8080 --host 0.0.0.0
```

- `--port`: Change port (default: 8000)
- `--host`: Allow external access (default: localhost)

_**Note:**_ Adding `--host 0.0.0.0` as an argument allows the server to be visible to other devices on the network. If the `server.py` is run on a lab computer and the questionnaire filled out on another device, it can be accessed via the lab computer's ip address like this `http://lab-computer-ip:8000/` 