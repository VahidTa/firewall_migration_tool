import os

from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask.templating import render_template
from werkzeug.utils import secure_filename

from resources.parser import main_parser
from resources import app_logger

logger = app_logger()

UPLOAD_FOLDER = 'configs/'
ALLOWED_EXTENSIONS = {'txt', 'log', 'csv'}

app = Flask(__name__, template_folder='resources/web/templates', static_folder='resources/web/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # check if the post request has the file part
        src_vendor = request.form.get('src_vendor')
        if request.form.get('type') == 'netconf':
            if src_vendor == 'srx':
                from resources.protocols.nc_conn import NcMGR
                acts = request.form.getlist('acts')
                action = request.form.get('action')
                nc_client = NcMGR()
                host = request.form.get('host')
                username = request.form.get('username')
                password = request.form.get('password')
                port = request.form.get('port')
                dst_vendor = request.form.get('dst_vendor')
                logger.info(f'Netconf started for {host} on port {port} ...')
                cfg = nc_client.junos_nc_conn(action, host, username, password, port, 'junos')
                if not cfg:
                    flash('Authentication error')
                    return redirect(request.url)
                elif cfg == 'other':
                    flash('Connection problem, please check network and info.')
                    return redirect(request.url)
                else:
                    logger.info('Conversion started ...')
                    main_parser(action, cfg, src_vendor, dst_vendor, acts)
                    logger.info(f'Creating files and links for {dst_vendor}')
                    return redirect(url_for('get_file', dirname=str(dst_vendor))) 
            else:
                flash(f'Not supported for {src_vendor}!')
                return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if src_vendor not in ['asa', 'forti']:
                acts = request.form.getlist('acts')
                action = request.form.get('action')
                if action == 'config' and not acts:
                    flash('Please select one checkbox!')
                    return redirect(request.url)

                dst_vendor = request.form.get('dst_vendor')

                logger.info('Conversion started ...')
                result = main_parser(action, filename, src_vendor, dst_vendor, acts)
                
                if not result:
                    flash('Something is wrong! check again')
                    return redirect(request.url)
                if result == 'no':
                    flash('The operation is not supported for this vendor!')
                    return redirect(request.url)
                logger.info(f'Creating files and links for {dst_vendor}')
                logger.info(50*'=')
                return redirect(url_for('get_file', dirname=str(dst_vendor)))
            else:
                flash('This conversion not supported yet.')
                return redirect(request.url)

        else:
            flash('File not supported. (txt, log, csv)')
            return redirect(request.url)
    return render_template('home.html')

@app.route('/exported/<dirname>/') # this is a job for GET, not POST
def get_file(dirname):
    dloads_dir = f'exported/{dirname}'
    dloads = os.listdir(dloads_dir)
    dloads_src = [f'/exported/{dirname}/{format(i)}' for i in dloads]
    return render_template('files.html', dloads=dloads, dloads_src=dloads_src, dirname=dirname)


@app.route('/exported/<dirname>/<filename>')
def download(dirname, filename):
    return send_from_directory(f'exported/{dirname}', filename)


@app.route('/exported/')
def exported():
    dloads_dir = 'exported/'
    dloads = os.listdir(dloads_dir)
    dloads_src = [f'/exported/{format(i)}' for i in dloads]
    return render_template('exported_vendor.html', dloads=dloads, dloads_src=dloads_src)


if __name__ == "__main__":
    app.run(host='0.0.0.0')