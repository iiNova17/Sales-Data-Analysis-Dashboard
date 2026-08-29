import pandas as pd
import matplotlib.pyplot as plt
def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error while reading the file.")
        return None

def inspect_data(data):
    """
    Inspect the data by displaying basic information and statistics.

    Parameters:
    data (pd.DataFrame): The DataFrame to inspect.
    """
    print("Data Information:")
    print(data.info())
    print("\nData Description:")
    print(data.describe())
    print("\nMissing Values:")
    print(data.isnull().sum())
    print("\nData Types:")
    print(data.dtypes)

"""
Data Types:
Row ID             int64
Order ID          object
Order Date        object
Ship Date         object
Ship Mode         object
Customer ID       object
Customer Name     object
Segment           object
Country           object
City              object
State             object
Postal Code      float64
Region            object
Product ID        object
Category          object
Sub-Category      object
Product Name      object
Sales            float64
"""

def preprocess_data(data):
    """
    Preprocess the data by handling missing values and encoding categorical variables.

    Parameters:
    data (pd.DataFrame): The DataFrame to preprocess.

    Returns:
    pd.DataFrame: The preprocessed DataFrame.
    """
    # Handle missing values
    data = data.dropna()  # Drop rows with missing values
    data = data.drop_duplicates()  # Drop duplicate rows

    # Convert date columns to datetime type
    data["Order Date"] = pd.to_datetime(data["Order Date"], errors='coerce', format='%d/%m/%Y')
    data['Order Year'] = data['Order Date'].dt.year
    data['Order Month'] = data['Order Date'].dt.to_period('M')
    data['Order DayOfWeek'] = data['Order Date'].dt.day_name()
    data["Ship Date"] = pd.to_datetime(data["Ship Date"], errors='coerce', format='%d/%m/%Y')
    # Convert categorical columns to category type
    category_cols = ['Ship Mode', 'Segment', 'Region', 'Category', 'Sub-Category']
    for col in category_cols:
        data[col] = data[col].astype('category')
    # Convert string columns to string type
    string_cols = [
    'Order ID', 'Customer ID', 'Customer Name', 'Country', 'City', 'State', 'Product ID', 'Product Name']
    for col in string_cols:
        data[col] = data[col].astype('string')
    # Convert Postal Code to integer type
    data['Postal Code'] = data['Postal Code'].astype('Int64')
    return data

def visualize_data(data):
    """
    Visualize the data using various plots.

    Parameters:
    data (pd.DataFrame): The DataFrame to visualize.
    """
    #Plotting sales over time
    plt.figure(figsize=(12, 6))
    data.groupby('Order Date')['Sales'].sum().plot()
    plt.title('Total Sales Over Time')
    plt.xlabel('Order Date')
    plt.ylabel('Total Sales')
    plt.grid()
    plt.show()
    #Plotting sales by category
    plt.figure(figsize=(12, 6))
    data.groupby('Category')['Sales'].sum().plot(kind='bar')
    plt.title('Total Sales by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Sales')
    plt.grid()
    plt.show()
    #Plotting sales by region
    plt.figure(figsize=(12, 6))
    data.groupby('Region')['Sales'].sum().plot(kind='bar')
    plt.title('Total Sales by Region')
    plt.xlabel('Region')
    plt.ylabel('Total Sales')
    plt.grid()
    plt.show()
    #Distribution of sales
    plt.figure(figsize=(12, 6))
    data['Sales'].plot(kind='hist', bins=50)
    plt.title('Distribution of Sales')
    plt.xlabel('Sales')
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()
    #Relationship between sales and order year
    plt.figure(figsize=(12, 6))
    data.groupby('Order Year')['Sales'].sum().plot()
    plt.title('Total Sales by Order Year')
    plt.xlabel('Order Year')
    plt.ylabel('Total Sales')
    plt.grid()
    plt.show()
    #Relationship between sales and order month
    plt.figure(figsize=(12, 6))
    data.groupby('Order Month')['Sales'].sum().plot()
    plt.title('Total Sales by Order Month')
    plt.xlabel('Order Month')
    plt.ylabel('Total Sales')
    plt.grid()
    plt.show()
    #plotting sales by ship mode
    plt.figure(figsize=(12, 6))
    data.groupby('Ship Mode')['Sales'].sum().plot(kind='bar')
    plt.title('Total Sales by Ship Mode')
    plt.xlabel('Ship Mode')
    plt.ylabel('Total Sales')
    plt.grid()
    plt.show()

def analyze_data(data):
    """
    Analyze the data to extract insights.

    Parameters:
    data (pd.DataFrame): The DataFrame to analyze.
    """
    # Top 5 products by sales
    top_products = data.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5)
    print("\nTop 5 Products by Sales:")
    print(top_products)
    
    # Top 5 customers by sales
    top_customers = data.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(5)
    print("\nTop 5 Customers by Sales:")
    print(top_customers)

    #Top 5 states by sales
    top_states = data.groupby('State')['Sales'].sum().sort_values(ascending=False).head(5)
    print("\nTop 5 States by Sales:")
    print(top_states)

    # Top 5 cities by sales
    top_cities = data.groupby('City')['Sales'].sum().sort_values(ascending=False).head(5)
    print("\nTop 5 Cities by Sales:")
    print(top_cities)

    # Sales by region
    sales_by_region = data.groupby('Region')['Sales'].sum()
    print("\nSales by Region:")
    print(sales_by_region)

    # Sales by category
    sales_by_category = data.groupby('Category')['Sales'].sum()
    print("\nSales by Category:")
    print(sales_by_category)

    # Sales by ship mode
    sales_by_ship_mode = data.groupby('Ship Mode')['Sales'].sum()
    print("\nSales by Ship Mode:")
    print(sales_by_ship_mode)

    # Top 5 sub-categories by sales
    top_sub_categories = data.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(5)
    print("\nTop 5 Sub-Categories by Sales:")
    print(top_sub_categories)

    #Outliers in sales
    Q1 = data['Sales'].quantile(0.25)
    Q3 = data['Sales'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = data[(data['Sales'] < (Q1 - 1.5 * IQR)) | (data['Sales'] > (Q3 + 1.5 * IQR))]
    print("\nOutliers in Sales:")
    print(outliers[['Order ID', 'Product Name', 'Sales']])

    # Top 5 months by sales
    top_months = data.groupby('Order Month')['Sales'].sum().sort_values(ascending=False).head(5)
    print("\nTop 5 Months by Sales:")
    print(top_months)
    insights = {
        "top_products": top_products,
        "top_customers": top_customers,
        "top_states": top_states,
        "top_cities": top_cities,
        "sales_by_region": sales_by_region,
        "sales_by_category": sales_by_category,
        "sales_by_ship_mode": sales_by_ship_mode,
        "top_sub_categories": top_sub_categories,
        "top_months": top_months,
        "outliers": outliers
    }
    return insights

def save_insights(insights, file_path):
    """
    Save the insights to a text file.

    Parameters:
    insights (dict): A dictionary containing the insights.
    file_path (str): The path to the output text file.
    """
    try:
        with open(file_path, 'w') as f:
            for category, products in insights.items():
                f.write(f"{category.capitalize()}:\n")
                for product, sales in products.items():
                    f.write(f"  {product}: {sales}\n")
        print(f"Insights saved to '{file_path}'.")
    except Exception as e:
        print(f"Error occurred while saving insights: {e}")

def save_preprocessed_data(data, file_path):
    """
    Save the preprocessed data to a CSV file.

    Parameters:
    data (pd.DataFrame): The DataFrame to save.
    file_path (str): The path to the output CSV file.
    """
    try:
        data.to_csv(file_path, index=False)
        print(f"Preprocessed data saved to '{file_path}'.")
    except Exception as e:
        print(f"Error occurred while saving preprocessed data: {e}")

def main():
    file_path = 'train.csv'  
    data = load_data(file_path)
    
    if data is not None:
        print("Data loaded successfully:")
        input("Press Enter to inspect the data...")
        inspect_data(data)
        input("Press Enter to preprocess the data...")
        data = preprocess_data(data)
        print("\nData Inspection after preprocessing:")
        inspect_data(data)
        input("Press Enter to visualize the data...")
        visualize_data(data)
        input("Press Enter to analyze the data...")
        insights = analyze_data(data)
        print("\nData analysis completed.")
        print("Type 1 to save the preprocessed data to a new CSV file,")
        print("Type 2 to save the insight data")
        print("Type 3 to save both the preprocessed data and the figures")
        print("Type any other key to exit the program")
        choice = input("Enter your choice: ")
        if choice == '1':
            save_preprocessed_data(data, 'preprocessed_data.csv')
        elif choice == '2':
            save_insights(insights, 'insights.txt')
        elif choice == '3':
            save_insights(insights, 'insights.txt')
            save_preprocessed_data(data, 'preprocessed_data.csv')
            print("Preprocessed data saved to 'preprocessed_data.csv' and insights saved to 'insights.txt'.")
        else:
            print("Exiting the program.")

if __name__ == "__main__":
    main()