#!/usr/bin/env python3
"""
Simple HTTP server for questionnaires.
Serves HTML files and saves submitted data to the data/ folder.

Usage:
    python server.py [--port PORT] [--host HOST]

Default: http://localhost:8000
"""

import os
import csv
import json
import argparse
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
HTML_DIR = os.path.join(SCRIPT_DIR, 'html_web_forms')  # HTML files are here


def get_bids_path(subject, session):
    """Create BIDS-compliant folder path: data/sub-{id}/ses-{n}/beh/"""
    bids_path = os.path.join(DATA_DIR, f'sub-{subject}', session, 'beh')
    os.makedirs(bids_path, exist_ok=True)
    return bids_path


class QuestionnaireHandler(SimpleHTTPRequestHandler):
    """Custom handler that serves files and saves form data."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HTML_DIR, **kwargs)

    def do_GET(self):
        """Serve GET requests for HTML files."""
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        """Handle POST requests for form submissions."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path != '/submit':
            self.send_error(404, 'Not Found')
            return

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            form_data = json.loads(post_data)
            
            subject = form_data.get('subject', 'unknown')
            session = form_data.get('session', 'ses-01')
            time = form_data.get('time', 'pre-sleep')
            questionnaire_type = form_data.get('type', 'unknown')
            
            bids_dir = get_bids_path(subject, session)
            filename = f"sub-{subject}_{session}_{time}_{questionnaire_type}.csv"
            filepath = os.path.join(bids_dir, filename)
            
            responses = form_data.get('responses', {})
            timestamp = datetime.now().isoformat()
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                
                if questionnaire_type == 'leeds':
                    writer.writerow(['subject', 'session', 'time', 'gts_difficulty', 'gts_speed', 'gts_sleepiness', 
                                    'qos_restless', 'qos_wakeful', 'afs_difficulty', 'afs_time', 
                                    'bfw_wakeup', 'bfw_current', 'bfw_balance', 'timestamp'])
                    writer.writerow([
                        subject, session, time,
                        responses.get('gts_difficulty', ''), responses.get('gts_speed', ''), 
                        responses.get('gts_sleepiness', ''),
                        responses.get('qos_restless', ''), responses.get('qos_wakeful', ''),
                        responses.get('afs_difficulty', ''), responses.get('afs_time', ''),
                        responses.get('bfw_wakeup', ''), responses.get('bfw_current', ''),
                        responses.get('bfw_balance', ''),
                        timestamp
                    ])
                    
                elif questionnaire_type == 'kss':
                    writer.writerow(['subject', 'session', 'time', 'KSS', 'timestamp'])
                    writer.writerow([subject, session, time, responses.get('KSS', ''), timestamp])
                    
                elif questionnaire_type == 'vams':
                    writer.writerow(['subject', 'experiment', 'session', 'time', 'happy', 'sad', 'calm', 'tense', 'energetic', 'sleepy', 'timestamp'])
                    writer.writerow([
                        subject,
                        form_data.get('experiment', ''),
                        session,
                        time,
                        responses.get('happy', ''), responses.get('sad', ''), responses.get('calm', ''),
                        responses.get('tense', ''), responses.get('energetic', ''), responses.get('sleepy', ''),
                        timestamp
                    ])
                    
                elif questionnaire_type == 'tes_side_effects':
                    stim_count = form_data.get('stim_count', '0')
                    date_val = form_data.get('date', '')
                    tes_related = form_data.get('tes_related', '')
                    experiment = form_data.get('experiment', '')
                    investigator = form_data.get('investigator', {})
                    
                    headers = ['subject', 'experiment', 'session', 'stim_count', 'date', 'tes_related']
                    row = [subject, experiment, session, stim_count, date_val, tes_related]
                    
                    symptom_ids = [
                        'itching', 'tingling', 'skin_redness', 'headache', 'pain', 'scalp_pain',
                        'neck_pain', 'burning_sensation', 'warmth_heat', 'metallic_iron_taste',
                        'fatigue_decreased_alertness', 'sleepiness', 'trouble_concentrating',
                        'acute_mood_change', 'nervousness_anxiety', 'discomfort',
                        'unpleasant_sensation', 'dizziness', 'nausea', 'visual_sensation'
                    ]
                    
                    for sid in symptom_ids:
                        data = responses.get(sid, {})
                        headers.extend([f'{sid}_present', f'{sid}_strength', f'{sid}_onset', f'{sid}_duration', f'{sid}_effect', f'{sid}_location', f'{sid}_electrode'])
                        row.extend([
                            'yes' if data.get('present') else 'no',
                            data.get('strength', ''),
                            data.get('onset', ''),
                            data.get('duration', ''),
                            data.get('effect', ''),
                            data.get('location', ''),
                            data.get('electrode', '')
                        ])
                    
                    headers.extend(['other_description', 'other_strength', 'other_onset', 'other_duration', 'other_effect', 'other_location', 'other_electrode'])
                    other_data = responses.get('other', {})
                    row.extend([
                        other_data.get('description', ''),
                        other_data.get('strength', ''),
                        other_data.get('onset', ''),
                        other_data.get('duration', ''),
                        other_data.get('effect', ''),
                        other_data.get('location', ''),
                        other_data.get('electrode', '')
                    ])
                    
                    headers.extend(['stim_type', 'intensity', 'duration', 'impedance', 'electrode_setup', 
                                   'electrode_count', 'electrode_shape', 'position_type'])
                    row.extend([
                        investigator.get('stim_type', ''),
                        investigator.get('intensity', ''),
                        investigator.get('duration', ''),
                        investigator.get('impedance', ''),
                        investigator.get('electrode_setup', ''),
                        investigator.get('electrode_count', ''),
                        investigator.get('electrode_shape', ''),
                        investigator.get('position_type', '')
                    ])
                    
                    electrodes = investigator.get('electrodes', [])
                    for i, electrode in enumerate(electrodes):
                        if investigator.get('position_type') == 'coordinates':
                            headers.extend([f'e{i+1}_x', f'e{i+1}_y', f'e{i+1}_z'])
                            row.extend([electrode.get('x', ''), electrode.get('y', ''), electrode.get('z', '')])
                        else:
                            headers.append(f'e{i+1}_position')
                            row.append(electrode.get('position', ''))
                    
                    headers.extend(['adverse_events', 'investigator_comments'])
                    row.extend([
                        investigator.get('adverse_events', '').replace('"', '""'),
                        investigator.get('comments', '').replace('"', '""')
                    ])
                    
                    headers.extend(['belief_sessions', 'belief_values'])
                    belief_data = form_data.get('belief', [])
                    if isinstance(belief_data, list):
                        belief_sessions = ';'.join([b.get('session', '') for b in belief_data])
                        belief_values = ';'.join([b.get('value', '') for b in belief_data])
                    else:
                        belief_sessions = belief_data.get('sessions', '')
                        belief_values = belief_data.get('values', '')
                    row.extend([belief_sessions, belief_values])
                    
                    headers.append('timestamp')
                    row.append(timestamp)
                    
                    writer.writerow(headers)
                    writer.writerow(row)
                    
                elif questionnaire_type == 'tacs_tis_sensation_testing':
                    stim_count = form_data.get('stim_count', '0')
                    date_val = form_data.get('date', '')
                    target_region = form_data.get('target_region', '')
                    region_side = form_data.get('region_side', '')
                    experiment = form_data.get('experiment', '')
                    tacs = form_data.get('tacs', {})
                    tis = form_data.get('tis', {})
                    comments = form_data.get('comments', '')
                    
                    headers = ['subject', 'experiment', 'session', 'stim_count', 'date', 'target_region', 'region_side']
                    row = [subject, experiment, session, stim_count, date_val, target_region, region_side]
                    
                    # Sensation list for checking
                    sensation_list = ['Pain', 'Stinging', 'Pinching', 'Itching', 'Heat', 'Pinprick',
                                     'Tingling', 'Vibrations', 'Pushing', 'Pulling', 'Pressure',
                                     'Pulse', 'Muscle spasm', 'Phosphenes', 'Hair prickle']
                    
                    # Helper to get checked sensations as comma-separated string
                    def get_sensations_list(sensations_data):
                        checked = []
                        for sensation in sensation_list:
                            sid = sensation.lower().replace(' ', '_').replace('/', '_')
                            if sensations_data.get(sid):
                                checked.append(sensation)
                        return ','.join(checked)
                    
                    # tACS section
                    headers.append('tacs_frequency')
                    row.append(tacs.get('frequency', ''))
                    
                    for electrode in ['e12', 'e34']:
                        electrode_data = tacs.get(electrode, {})
                        sensations = electrode_data.get('sensations', {})
                        prefix = f'tacs_{electrode}'
                        
                        headers.extend([f'{prefix}_threshold', f'{prefix}_max_applied', f'{prefix}_impedance', 
                                       f'{prefix}_sensations', f'{prefix}_location', f'{prefix}_other'])
                        row.extend([
                            electrode_data.get('threshold', ''),
                            electrode_data.get('max_applied', ''),
                            electrode_data.get('impedance', ''),
                            get_sensations_list(sensations),
                            electrode_data.get('location', ''),
                            sensations.get('other', '')
                        ])
                    
                    # TIS section
                    headers.extend(['tis_carrier_frequency', 'tis_modulation_frequency'])
                    row.extend([tis.get('carrier_frequency', ''), tis.get('modulation_frequency', '')])
                    
                    for electrode in ['e12', 'e34']:
                        electrode_data = tis.get(electrode, {})
                        sensations = electrode_data.get('sensations', {})
                        prefix = f'tis_{electrode}'
                        
                        headers.extend([f'{prefix}_threshold', f'{prefix}_max_applied', f'{prefix}_impedance', 
                                       f'{prefix}_sensations', f'{prefix}_location', f'{prefix}_other'])
                        row.extend([
                            electrode_data.get('threshold', ''),
                            electrode_data.get('max_applied', ''),
                            electrode_data.get('impedance', ''),
                            get_sensations_list(sensations),
                            electrode_data.get('location', ''),
                            sensations.get('other', '')
                        ])
                    
                    headers.extend(['comments', 'timestamp'])
                    row.extend([comments.replace('"', '""'), timestamp])
                    
                    writer.writerow(headers)
                    writer.writerow(row)
                    
                elif questionnaire_type == 'sleep_diary':
                    headers = ['subject', 'experiment', 'session', 'time', 'date', 'bedtime', 'sleep_onset_latency', 
                              'awakenings', 'awake_time', 'wake_time', 'rise_time', 'alarm_used',
                              'quality', 'refreshed', 'caffeine', 'alcohol', 'napped', 'nap_duration', 
                              'notes', 'timestamp']
                    row = [
                        subject,
                        form_data.get('experiment', ''),
                        session,
                        time,
                        form_data.get('date', ''),
                        form_data.get('bedtime', ''),
                        form_data.get('sleep_onset_latency', '0'),
                        form_data.get('awakenings', '0'),
                        form_data.get('awake_time', '0'),
                        form_data.get('wake_time', ''),
                        form_data.get('rise_time', ''),
                        form_data.get('alarm_used', 'no'),
                        form_data.get('quality', '3'),
                        form_data.get('refreshed', '3'),
                        form_data.get('caffeine', '0'),
                        form_data.get('alcohol', '0'),
                        form_data.get('napped', 'no'),
                        form_data.get('nap_duration', '0'),
                        form_data.get('notes', '').replace('"', '""'),
                        timestamp
                    ]
                    writer.writerow(headers)
                    writer.writerow(row)
                    
                elif questionnaire_type == 'mctq':
                    headers = ['subject', 'experiment', 'session', 'regular_work', 'work_days',
                              'work_bedtime', 'work_sleep_ready', 'work_sleep_latency', 'work_wake_time',
                              'work_rise_latency', 'work_alarm', 'work_alarm_before',
                              'free_bedtime', 'free_sleep_ready', 'free_sleep_latency', 'free_wake_time',
                              'free_rise_latency', 'free_alarm', 'free_reasons', 'free_reason_types',
                              'free_reason_other', 'timestamp']
                    row = [
                        subject,
                        form_data.get('experiment', ''),
                        session,
                        form_data.get('regular_work', ''),
                        form_data.get('work_days', ''),
                        form_data.get('work_bedtime', ''),
                        form_data.get('work_sleep_ready', ''),
                        form_data.get('work_sleep_latency', '0'),
                        form_data.get('work_wake_time', ''),
                        form_data.get('work_rise_latency', '0'),
                        form_data.get('work_alarm', ''),
                        form_data.get('work_alarm_before', ''),
                        form_data.get('free_bedtime', ''),
                        form_data.get('free_sleep_ready', ''),
                        form_data.get('free_sleep_latency', '0'),
                        form_data.get('free_wake_time', ''),
                        form_data.get('free_rise_latency', '0'),
                        form_data.get('free_alarm', ''),
                        form_data.get('free_reasons', ''),
                        form_data.get('free_reason_types', ''),
                        form_data.get('free_reason_other', '').replace('"', '""'),
                        timestamp
                    ]
                    writer.writerow(headers)
                    writer.writerow(row)
                    
                else:
                    headers = ['subject', 'session', 'time'] + list(responses.keys()) + ['timestamp']
                    writer.writerow(headers)
                    row = [subject, session, time] + list(responses.values()) + [timestamp]
                    writer.writerow(row)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'success': True, 'filename': filename})
            self.wfile.write(response.encode())
            
            print(f"[SAVED] {filename}")
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'success': False, 'error': str(e)})
            self.wfile.write(response.encode())
            print(f"[ERROR] {e}")

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    parser = argparse.ArgumentParser(description='Serve questionnaires and save data locally')
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on (default: 8000)')
    parser.add_argument('--host', type=str, default='localhost', help='Host to bind to (default: localhost)')
    args = parser.parse_args()
    
    server = HTTPServer((args.host, args.port), QuestionnaireHandler)
    
    print(f"\n{'='*60}")
    print("QUESTIONNAIRE SERVER")
    print(f"{'='*60}")
    print(f"\nOpen in browser:")
    print(f"  http://{args.host}:{args.port}/")
    print(f"\nQuestionnaire links available on the landing page.")
    print(f"\nData saved to: {DATA_DIR}")
    print(f"\nPress Ctrl+C to stop the server")
    print(f"{'='*60}\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        server.shutdown()


if __name__ == '__main__':
    main()