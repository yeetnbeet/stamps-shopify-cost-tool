# Shopify Shipping Cost Tool

The Shopify Shipping Cost tool is a command-line interface (CLI) utility designed to fetch order details from a Shopify store, process shipping costs, and provide a comprehensive breakdown. Developed with efficiency and user-friendliness in mind, it offers a streamlined experience for store managers and developers alike.

*Designed as a script to make future analytics faster*
*Shipping Export: is assumed format from stamps.com*
*Order Export: is assumed format from shopify.admin*

## Features

- Fetch orders directly from Shopify using the API.
- Process and map order data with associated shipping costs.
- Generate a comprehensive breakdown of shipping costs vs. revenue.
- Easy-to-use command-line interface with argument flexibility.

## Prerequisites

1. **Shopify Token**: To use this tool, you'll need a Shopify token with **Order Read** capabilities. This token allows the tool to fetch order details from your Shopify store. Please refer to Shopify's official documentation on how to obtain this token.
   
2. **Python**: Ensure you have Python 3.x installed.

3. **Dependencies**: This tool utilizes several Python libraries. Make sure to install them using `pip`:
   ```bash
   pip install requests pandas
   ```

## Usage

1. Clone the repository or download the tool:
   ```bash
   git clone https://github.com/yeetnbeet/stamps-shopify-cost-tool
   ```

2. Navigate to the directory:
   ```bash
   cd path_to_directory
   ```

3. Run the tool using Python:
   ```bash
   python script_name.py --shopify_token YOUR_TOKEN --store_name YOUR_STORE_NAME
   ```

### Command-Line Arguments

- `--shopify_token`: Your Shopify API token with Order Read capabilities.
- `--store_name`: The name of your Shopify store.
- `--shipping_csv_path`: (Optional) Path to the shipping CSV. Defaults to 'stamps.csv'.
- `--order_csv_path`: (Optional) Path to the order CSV. Defaults to 'orders.csv'.
- `--start_date`: (Optional) Start date in ISO format. Defaults to the date 6 months ago from today.

## Important Notes

- Ensure your token has the necessary permissions. Without the Order Read capability, the tool cannot fetch order details.
  
- Always protect your Shopify token. Do not expose it in shared or public environments.

## Feedback & Contributions

Feedback, bug reports, and pull requests are welcome. For major changes, please open an issue first to discuss the intended change.

## License

[MIT License](LICENSE)

---

You can add or customize this template as needed. Make sure to include any additional sections that may be relevant, such as a "Known Issues" or "Future Enhancements" section.