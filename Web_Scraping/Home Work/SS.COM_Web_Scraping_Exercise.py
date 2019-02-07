




# TODO: RCS exercise. SS.COM web scraping.

# In this exercise we have to make pandas dataframe list of all wood sellers from all Latvian regions. And save the pandas data frame to excel file.

import requests
from bs4 import BeautifulSoup as soup
import pandas as pd


url = "https://www.ss.com/lv/real-estate/wood/"
req = requests.get(url)
soup_obj = soup(req.text, 'html.parser')
regions = soup_obj.find_all('a', {'class': 'a_category'})
base_url = 'https://www.ss.com'

# Create list with urls from every region.
urllist = [base_url + region['href'] for region in regions]

# Add every regionurl 'sell/' at the end of it, as we want to get only sellers.
sellers = [el + 'sell/' for el in urllist]


# Create empty data frame to which we will append our data to.
appended_df = pd.DataFrame()

# Main for loop.
for i in range(len(sellers)):
    req_region = requests.get(sellers[i])
    pages_soup_obj = soup(req_region.text, 'html.parser')
    region_page_text_list = pages_soup_obj.find_all(text=True)

    # Check if there is any listings in this region.
    if 'Sludinājumi dotajā kategorijā nav atrasti' in region_page_text_list:
        continue

    else:
        # Check if there is pagination 'div'.
        pages_div = pages_soup_obj.find_all('div', {'class': 'td2'})

        # If region has more than one page.
        if len(pages_div) != 0:

            # Find how many pages region has.
            finding_number_of_pages = pages_div[0].find('a')
            splited_html_list = str(finding_number_of_pages).split('.html')
            splited_html_list2 = splited_html_list[0].split('page')
            number_of_pages = splited_html_list2[-1]

            # Iterate through all the region's pages and append them to main data frame.
            for j in range(int(number_of_pages)):

                # If it is first page.
                if j == 0:

                    # Find the necessary data table from HTML by providing all table attributes.
                    region_df_table_list = pd.read_html(req_region.text, attrs={'align': 'center', 'cellpadding': "2",
                                                                                'cellspacing': "0", 'border': "0",
                                                                                'width': "100%"})
                    region_df_table = region_df_table_list[0]

                    # Slice desired information from data frame.
                    region_sliced_table = region_df_table.iloc[1:, 2:]
                    region_sliced_table.columns = ['Description', 'District', 'Area (ha)', 'Price (€)']
                    appended_df = appended_df.append(region_sliced_table, ignore_index=True)

                # If it is not the first page, search by adding 'page{j + 1}.html' at the end of the URL.
                else:
                    req_region = requests.get(sellers[i] + f'page{j + 1}.html')
                    region_df_table_list = pd.read_html(req_region.text, attrs={'align': 'center', 'cellpadding': "2",
                                                                                'cellspacing': "0", 'border': "0",
                                                                                'width': "100%"})
                    region_df_table = region_df_table_list[0]
                    region_sliced_table = region_df_table.iloc[1:, 2:]
                    region_sliced_table.columns = ['Description', 'District', 'Area (ha)', 'Price (€)']
                    appended_df = appended_df.append(region_sliced_table, ignore_index=True)

        # If region has only one page.
        else:
            region_df_table_list = pd.read_html(req_region.text,
                                                attrs={'align': 'center', 'cellpadding': "2",
                                                       'cellspacing': "0", 'border': "0",
                                                       'width': "100%"})
            region_df_table = region_df_table_list[0]
            region_sliced_table = region_df_table.iloc[1:, 2:]
            region_sliced_table.columns = ['Description', 'District', 'Area (ha)', 'Price (€)']
            appended_df = appended_df.append(region_sliced_table, ignore_index=True)



# To be able to sort by price, 'Cena' column's values must be modified and made into integers.
# 1. Striped ' €' and ',' from all price values.
integer_prices_df = appended_df['Price (€)'].map(lambda x: x.rstrip(' €').replace(',', ''))

# 2. Converted all values to integer.
integer_prices_df = pd.to_numeric(integer_prices_df)

# 3. Replace old 'Cena' column values with newly created Series or single column DataFrame 'integer_prices_df' column.
appended_df.loc[:, 'Price (€)'] = integer_prices_df



# To be able to sort by area, 'Platība (ha)' column's values must be modified and made into integers.
# For some reason there are some area fields with values in square meters instead in hectares. These fields must be converted to hectares.
# There is also some fields with some random integers without the unit. Replace them with None.

def area_func(x):
    if 'm' in x:
        ha_int = float(x.split(' ')[0]) / 10000
        return ha_int
    elif 'ha' in x:
        ha_int = float(x.replace(' ha.', ''))
        return ha_int
    else:
        return None


integer_area_df = appended_df['Area (ha)'].map(lambda x: area_func(x))
integer_area_df = pd.to_numeric(integer_area_df)
appended_df.loc[:, 'Area (ha)'] = integer_area_df



# Create additional column for price per area unit values with column name 'Price/Area (€/ha)'.
# 1. Create df from price column.
price_df = appended_df.loc[:, 'Price (€)']

# 2. Create df from area column. Replace NaN values with 1 for division purposes.
area_df = appended_df.loc[:, 'Area (ha)'].fillna(1)

# 3. Divide both dfs. Change division values from floats to ints.
price_per_area_df = price_df.divide(area_df).astype(int)

appended_df['Price/Area (€/ha)'] = price_per_area_df





# # Write all modified pandas dataframe to excel file.
appended_df.to_excel("ss.com_wood_sellers_in_latvia.xlsx")