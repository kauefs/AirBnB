import  numpy            as np
import  pandas           as pd
import  pydeck           as pdk
import  seaborn          as sns
import streamlit         as st
import matplotlib.pyplot as plt
from   pydeck.data_utils import compute_view
from   wordcloud         import WordCloud, STOPWORDS, ImageColorGenerator
from   PIL import Image
st.set_page_config(page_title='SYD', page_icon='🌃')
# DATA:
DATA         = 'dataset/AirBnB•SYD20230606.csv.gz'
@st.cache_data
def LoadData():
    rename   = {'name'                          :'listing',
                'host_name'                     :'host'   ,
                'room_type'                     :'room'   ,
                'minimum_nights'                :'nights' ,
                'number_of_reviews'             :'reviews',
                'availability_365'              :'365'    ,
                'number_of_reviews_ltm'         :'ltm'    } # Last Twelve Months
    data      = pd.read_csv(DATA)
    data      = data.rename(columns=rename)
# Cleaning:
    data      = data.fillna({'host' :'HOST'})
    data      = data.fillna({'last' :     0})
    data      = data.fillna({'month':     0})
    data      = data.dropna(subset=['description'], axis=0)
    data.price=data.price.replace('[\$,]', '', regex=True).astype(float)
# OutLiers:
    data.drop(data[data.price   > 600].index, axis=0, inplace=True)
    data.drop(data[data.nights  >  90].index, axis=0, inplace=True)
    data.drop(data[data.reviews >  50].index, axis=0, inplace=True)
# Selecting:
    columns  = ['listing'      ,
                'host'         ,
                'neighbourhood',
                'latitude'     ,
                'longitude'    ,
                'room'         ,
                'price'        ,
                'nights'       ,
                'reviews'      ,
                '365'          ,
                'ltm'          ,
                'description'  ]    
    data     = data[list(columns)]
    return data
df           = LoadData()
hood         = df.neighbourhood.unique().tolist()
room         = df.room.unique().tolist()
# SIDE:
st.sidebar.success(  'Sydney Airbnb')
st.sidebar.header(   'Inside Airbnb')
st.sidebar.subheader('SYDNEY       ')
st.sidebar.markdown( 'Data Analysis')
st.sidebar.write('Data Base Date: 2023.06.06')
# PlaceHolder for Table:
table        = st.sidebar.empty()
# PlaceHolder for Filtered Listings:
SideBarInfo  = st.sidebar.empty()
# MultiSelect for NeighBourHood:
FilteredHood = st.sidebar.multiselect(label  = 'NeighBourHood:',
                                      options=  hood,
                                      default=['Sydney, New South Wales, Australia'])
# MultiSelect for RoomType:
FilteredRoom = st.sidebar.multiselect(label  = 'RoomType:',
                                      options=  room,
                                      default=['Entire home/apt','Private room','Shared room','Hotel room'])
# Price Slider Selection:
FilteredPrice= st.sidebar.slider('Price:', 0.01, 599.99, 255.75, step=None)
# Filtered Data:
FilteredDF   = df[(df.neighbourhood.isin(FilteredHood)) & (df.room.isin(FilteredRoom)) & (df.price <= FilteredPrice)]
# Updating PlaceHoder:
SideBarInfo.info('{} Filtered Listings'.format(FilteredDF.shape[0]))
# MAIN:
st.title('Inside Sydney Airbnb')
# WordCloud:
#SYD         =  pd.read_csv('datasets/SYD20230606AirBnB.csv.gz')
#select      =['description']
#text        =  SYD[list(select)]
#description =  text.dropna(subset=['description'], axis=0)['description']
with st.spinner('Loading…'):
    all         = ' '.join(words for words in FilteredDF['description'])
    StopWords   =  set(STOPWORDS)
    StopWords.update(['b', 'PID', 'will', 'number', 'br', 'EXT'])
    mask        =  np.array(Image.open('img/sydney.jpg'))
    WordCloud   =  WordCloud(stopwords=StopWords,
                             mask=mask,
                             colormap='autumn',
                             background_color='black',
                            #relative_scaling=.5,
                             max_font_size=None,
                             max_words=750,
                             contour_width=0,
                             contour_color='black',
                             width=750, height=750, margin=0).generate(all)
fig, ax = plt.subplots(facecolor='k')
ax      = plt.imshow(WordCloud, interpolation='bilinear')
ax      = plt.axis('off')
st.pyplot(fig,clear_figure=None,use_container_width=True)
# Table:
st.subheader('DATA')
st.markdown( '''    Source: [Inside Airbnb](http://insideairbnb.com/get-the-data.html)''')
st.markdown(f'''➡️  Showing {'**{}**'.format(FilteredDF.shape[0])} **{', '.join(FilteredRoom)}** in **{', '.join(FilteredHood)}** under **AUD {FilteredPrice}**:''')
if table.checkbox('Show Table Data', value=True):st.write(FilteredDF)
# Columns:
L, R = st.columns(2)
with L:
    st.subheader('Correlation Matrix')
    mtx       = FilteredDF[['price','nights','reviews']].corr()
    fig1, ax1 = plt.subplots()
    ax1       = sns.heatmap(mtx,
                            fmt       ='.2f',
                            cbar      = True,
                            annot     = True,
                            square    = True,
                            cmap      ='bone',
                            linewidths=      1,
                            linecolor ='white')
    st.pyplot(fig1,
              clear_figure=None,
              use_container_width=True)
with R:
    st.subheader(  'Heat Map')
    corr      = FilteredDF[['price','nights','reviews']].corr()
    fig2, ax2 = plt.subplots()
    ax2       = sns.heatmap(corr,
                            fmt       ='.2f',
                            cbar      = True,
                            annot     = True,
                            square    = True,
                            cmap      ='binary',
                            linewidths=      1,
                            linecolor ='white')
    st.pyplot(fig2,
              clear_figure=None,
              use_container_width=True)
# MAP:
st.sidebar.write('Map Options:')
if  st.sidebar.checkbox('3D', value=True):
    st.subheader('3D Map')
#initial = compute_view(FilteredDF[['longitude','latitude']], 0.25)
    st.pydeck_chart(pdk.Deck(layers=[#pdk.Layer('HexagonLayer',
                                     #           data=FilteredDF,
                                     #           disk_resolution=  10,
                                     #           radius         =  75,
                                     #           get_position   =['longitude','latitude'],
                                     #           get_fill_color =[255, 255, 255, 255],  # RGBA
                                     #           get_line_color =[  0,   0,   0,   0],
                                     #           auto_highlight = True,
                                     #           elevation_scale=  50,
                                     #           elevation_range=[  0, 100] ,
                                     #           get_elevation  = 'price'   ,
                                     #           pickable=True,
                                     #           extruded=True,
                                     #           coverage=1),
                                     #pdk.Layer('ScatterplotLayer',
                                     #           data          =  FilteredDF,
                                     #           get_position  =['longitude','latitude'],
                                     #           auto_highlight=  True,
                                     #           get_fill_color=[255, 255, 255, 55],    # RGBA
                                     #           get_line_color=[  0,   0,   0,  0],
                                     #           get_radius    =1,
                                     #           pickable      =       True),
                                     pdk.Layer('ColumnLayer',
                                                data           =  FilteredDF,
                                                radius         =  15,
                                                disk_resolution=  15,
                                                get_position   =['longitude','latitude'],
                                                get_elevation  = 'price'    ,
                                                elevation_scale= 7.5,
                                                elevation_range=[0, 75],
                                                get_fill_color =[255, 255, 255, 55],    # RGBA
                                                get_line_color =[  0,   0,   0,  0],
                                                auto_highlight =  True,
                                                pickable       =  True,
                                                extruded       =  True,
                                                coverage       =   1)],
                             views=[{'@@type':'MapView', 'controller':True}],
                             map_style=pdk.map_styles.SATELLITE,
                             api_keys = None ,
                             initial_view_state=pdk.ViewState(#initial,
                                                              longitude=151.20,
                                                              latitude =-33.88,
                                                              zoom     = 12   ,
                                                              min_zoom = None ,
                                                              max_zoom = None ,
                                                              pitch    = 75   ,
                                                              bearing  = 45  ),
                             width       ='100%',
                             height      =  500 ,
                             tooltip     ={'text':'AUD {price}'},
                             description = None ,
                             effects     = None ,
                             map_provider='mapbox', #'carto'
                             parameters  = None ))
if  st.sidebar.checkbox('2D'):
    st.subheader('2D Map:')
    st.map(FilteredDF)
st.sidebar.divider()
with st.sidebar.container():
     C1,  C2,  C3 = st.columns(3)
     with C1:st.empty()
     with C2:st.markdown('''©2023™''')
     with C3:st.empty()
st.toast('SYD!', icon='🌃')
