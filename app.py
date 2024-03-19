# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np
import os

filename = 'KNN.pkl'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('main.html', prediction=None)


@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':

        flag_S0 = int(request.form['flag_S0'])
        serror_rate = float(request.form.get('serror_rate'))
        diff_srv_rate = float(request.form.get('diff_srv_rate'))
        srv_serror_rate = float(request.form['srv_serror_rate'])
        dst_host_serror_rate = float(request.form['dst_host_serror_rate'])
        dst_host_srv_serror_rate= float(request.form.get('dst_host_srv_serror_rate'))
        dst_host_diff_srv_rate = float(request.form['dst_host_diff_srv_rate'])
        count= int(request.form['count'])
        service= request.form.get('service_private')
        
        # Map 'service' to 'service_private' based on the selected option
        if service == 'private':
            service_private = 1
        else:
            service_private = 0
        
        dst_host_count = int(request.form['dst_host_count'])
        rerror_rate = float(request.form.get('rerror_rate'))
        srv_rerror_rate = float(request.form['srv_rerror_rate'])
        dst_host_rerror_rate = float(request.form.get('dst_host_rerror_rate'))
        protocol_type = request.form.get('protocol_type_icmp')

        if protocol_type == 'icmp':
            protocol_type_icmp = 1
        else:
            protocol_type_icmp = 0
        
        dst_host_srv_rerror_rate = float(request.form.get('dst_host_srv_rerror_rate'))
        
        data = np.array([[flag_S0,serror_rate,diff_srv_rate,srv_serror_rate,dst_host_serror_rate,dst_host_srv_serror_rate,dst_host_diff_srv_rate,count,service_private,dst_host_count,rerror_rate,
srv_rerror_rate,dst_host_rerror_rate,protocol_type_icmp,dst_host_srv_rerror_rate]])
        my_prediction = model.predict(data)

        save_input_data(data)
        return render_template('main.html', prediction=my_prediction, input_data=data)

    return render_template('main.html', prediction=None)
        # return render_template('result.html', prediction=my_prediction,input_data=data)
        
def save_input_data(data):
    # Define a filename for the saved input data
    input_data_filename = 'input_data.txt'
    
    # Check if the file exists and append the data
    if os.path.exists(input_data_filename):
        with open(input_data_filename, 'a') as file:
            np.savetxt(file, data, delimiter=',', fmt='%f')
    else:
        # Create a new file and save the data
        with open(input_data_filename, 'w') as file:
            np.savetxt(file, data, delimiter=',', fmt='%f')

def save_output_data(data, prediction):
    # Define a filename for the saved output data
    output_data_filename = 'output_data.txt'

    with open(output_data_filename, 'a') as file:
        # Save the input data and prediction
        np.savetxt(file, data, delimiter=',', fmt='%f')
        file.write(f"Prediction: {prediction}\n")

        # Optionally, you can add a separator for readability
        file.write("\n")

if __name__ == '__main__':
	app.run(debug=False,host='0.0.0.0')

