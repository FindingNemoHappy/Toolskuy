from flask import Flask, render_template, request, send_file
import requests
from datetime import datetime
import pandas as pd
from io import BytesIO

app = Flask(__name__)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

@app.route('/download_excel', methods=['GET'])
def download_excel():
    timeMin = request.args.get('timeMin', '2024-01-01')
    timeMax = request.args.get('timeMax', '2024-07-30')
    filterJudul = request.args.get('filterJudul', '')

    url = f"https://clients6.google.com/calendar/v3/calendars/c_qnn6qqu95c7j0hkh9lfh870gl8@group.calendar.google.com/events?calendarId=c_qnn6qqu95c7j0hkh9lfh870gl8%40group.calendar.google.com&singleEvents=true&eventTypes=default&eventTypes=focusTime&eventTypes=outOfOffice&timeZone=Asia%2FJakarta&maxAttendees=1&maxResults=1000&sanitizeHtml=true&timeMin={timeMin}T00%3A00%3A00%2B07%3A00&timeMax={timeMax}T00%3A00%3A00%2B07%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs"

    response = requests.get(url)

    results = []
    if response.status_code == 200:
        data = response.json()
        for event in data.get('items', []):
            kegiatan = event.get('summary', 'Tidak ada kegiatan')
            waktu = event.get('start', {}).get('dateTime', 'Tidak ada waktu')
            deskripsi = event.get('description', '')

            if 'T' in waktu:
                tanggal = waktu.split('T')[0]
                tanggal_obj = parse_date(tanggal)
            else:
                tanggal_obj = None

            lines = deskripsi.split('\n')
            judul = None
            turnitin_link = None

            for line in lines:
                if line.startswith('Judul:'):
                    judul = line.split('Judul: ')[-1].strip()
                elif line.startswith('Turnitin:'):
                    turnitin_link = line.split('Turnitin: ')[-1].strip()

            if filterJudul:
                keywords = filterJudul.lower().split()
                if all(keyword in (judul.lower() if judul else '') for keyword in keywords):
                    if judul and turnitin_link:
                        results.append({
                            'kegiatan': kegiatan,
                            'tanggal': tanggal_obj,
                            'judul': judul,
                            'turnitin_link': turnitin_link
                        })
                    else:
                        results.append({
                            'kegiatan': kegiatan,
                            'informasi': 'Informasi tidak lengkap atau tidak ditemukan.'
                        })
            else:
                if judul and turnitin_link:
                    results.append({
                        'kegiatan': kegiatan,
                        'tanggal': tanggal_obj,
                        'judul': judul,
                        'turnitin_link': turnitin_link
                    })
                else:
                    results.append({
                        'kegiatan': kegiatan,
                        'informasi': 'Informasi tidak lengkap atau tidak ditemukan.'
                    })

        results = sorted(results, key=lambda x: x['tanggal'] if x['tanggal'] else datetime.min)

        df = pd.DataFrame(results)
        df['tanggal'] = df['tanggal'].apply(lambda x: x.strftime('%Y-%m-%d') if x else '')

        excel_file = BytesIO()
        df.to_excel(excel_file, index=False, engine='openpyxl')
        excel_file.seek(0)

        excel_filename = f"calendar_data_{timeMin}_{timeMax}.xlsx"
        return send_file(excel_file, download_name=excel_filename, as_attachment=True)

    else:
        results = [{'error': f"Permintaan gagal dengan kode status {response.status_code}"}]
        jumlah_data = 0

    return render_template('index.html', results=results, jumlah_data=jumlah_data, timeMin=timeMin, timeMax=timeMax, filterJudul=filterJudul)

@app.route('/', methods=['GET'])
def index():
    timeMin = request.args.get('timeMin', '2024-01-01')
    timeMax = request.args.get('timeMax', '2024-07-30')
    filterJudul = request.args.get('filterJudul', '')

    url = f"https://clients6.google.com/calendar/v3/calendars/c_qnn6qqu95c7j0hkh9lfh870gl8@group.calendar.google.com/events?calendarId=c_qnn6qqu95c7j0hkh9lfh870gl8%40group.calendar.google.com&singleEvents=true&eventTypes=default&eventTypes=focusTime&eventTypes=outOfOffice&timeZone=Asia%2FJakarta&maxAttendees=1&maxResults=1000&sanitizeHtml=true&timeMin={timeMin}T00%3A00%3A00%2B07%3A00&timeMax={timeMax}T00%3A00%3A00%2B07%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs"

    response = requests.get(url)

    results = []
    if response.status_code == 200:
        data = response.json()
        for event in data.get('items', []):
            kegiatan = event.get('summary', 'Tidak ada kegiatan')
            waktu = event.get('start', {}).get('dateTime', 'Tidak ada waktu')
            deskripsi = event.get('description', '')

            if 'T' in waktu:
                tanggal = waktu.split('T')[0]
                tanggal_obj = parse_date(tanggal)
            else:
                tanggal_obj = None

            lines = deskripsi.split('\n')
            judul = None
            turnitin_link = None

            for line in lines:
                if line.startswith('Judul:'):
                    judul = line.split('Judul: ')[-1].strip()
                elif line.startswith('Turnitin:'):
                    turnitin_link = line.split('Turnitin: ')[-1].strip()

            if filterJudul:
                keywords = filterJudul.lower().split()
                if all(keyword in (judul.lower() if judul else '') for keyword in keywords):
                    if judul and turnitin_link:
                        results.append({
                            'kegiatan': kegiatan,
                            'tanggal': tanggal_obj,
                            'judul': judul,
                            'turnitin_link': turnitin_link
                        })
                    else:
                        results.append({
                            'kegiatan': kegiatan,
                            'informasi': 'Informasi tidak lengkap atau tidak ditemukan.'
                        })
            else:
                if judul and turnitin_link:
                    results.append({
                        'kegiatan': kegiatan,
                        'tanggal': tanggal_obj,
                        'judul': judul,
                        'turnitin_link': turnitin_link
                    })
                else:
                    results.append({
                        'kegiatan': kegiatan,
                        'informasi': 'Informasi tidak lengkap atau tidak ditemukan.'
                    })

        results = sorted(results, key=lambda x: x['tanggal'] if x['tanggal'] else datetime.min)
        jumlah_data = len(results)
    else:
        results = [{'error': f"Permintaan gagal dengan kode status {response.status_code}"}]
        jumlah_data = 0

    return render_template('index.html', results=results, jumlah_data=jumlah_data, timeMin=timeMin, timeMax=timeMax, filterJudul=filterJudul)

if __name__ == '__main__':
    app.run(debug=True)
