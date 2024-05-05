# Function to upload PDF data
def upload_data():
    uploaded_file = input("Upload Monthly Report (CSV): ",Monthly report.csv)
    if uploaded_file.endswith('.csv'):
        with open(uploaded_file, 'r') as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            data = [line.strip().split(',') for line in lines[1:]]
            df = {header: [] for header in headers}
            for row in data:
                for i, value in enumerate(row):
                    df[headers[i]].append(value)
            return df
    else:
        print("Please upload a CSV file.")

# Function to calculate derived fields
def calculate_fields(df, selected_fields):
    # Calculate derived fields
    if "Net Inflow/Outflow" in selected_fields:
        df['Net Inflow/Outflow'] = [float(df['Funds Mobilized'][i]) - float(df['Repurchase/Redemption'][i]) for i in range(len(df['Funds Mobilized']))]
    if "Net Asset under Management per Scheme" in selected_fields:
        df['Net AUM per Scheme'] = [float(df['Net Assets Under Management'][i]) / float(df['No. of Schemes'][i]) for i in range(len(df['Net Assets Under Management']))]
    if "Net Inflow/Outflow per Scheme" in selected_fields:
        df['Net Inflow/Outflow per Scheme'] = [float(df['Net Inflow/Outflow'][i]) / float(df['No. of Schemes'][i]) for i in range(len(df['Net Inflow/Outflow']))]
    return df

# Function to generate dynamic charts
def generate_charts(df, selected_fields):
    for field in selected_fields:
        if field != "Date":
            print(field)
            for scheme in df['Scheme']:
                values = [float(df[field][i]) for i in range(len(df[field])) if df['Scheme'][i] == scheme]
                print(scheme, values)

# Main function to run the Streamlit app
def main():
    print("Mutual Fund Data Analysis App")
    
    # Data upload section
    print("1. Data Upload Functionality")
    df = upload_data()
    
    if df is not None:
        # Scheme selection section
        print("2. Scheme Selection")
        selected_schemes = input("Select Mutual Fund Scheme(s): ").split(',')

        # Field selection and calculation section
        print("3. Field Selection and Calculation")
        selected_fields = input("Select Data Field(s): ").split(',')
        df = calculate_fields(df, selected_fields)

        # Dynamic reporting section
        print("4. Dynamic Reporting")
        print("Selected Data:")
        print(df)

        # Generate dynamic charts
        generate_charts(df, selected_fields)

        # Download capability section
        print("5. Download Capability")
        download_report = input("Download Report as CSV? (yes/no): ")
        if download_report.lower() == "yes":
            with open('mutual_fund_report.csv', 'w') as file:
                headers = ','.join(df.keys())
                file.write(headers + '\n')
                for i in range(len(df['Date'])):
                    row = ','.join([str(df[key][i]) for key in df.keys()])
                    file.write(row + '\n')
            print("CSV report downloaded as 'mutual_fund_report.csv'.")

if __name__ == "__main__":
    main()
