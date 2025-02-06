import  streamlit              as    st
import      numpy              as    np
import     pandas              as    pd
import     pydeck              as    pdk
import    seaborn              as    sns
import matplotlib.pyplot       as    plt
from       pydeck.data_utils import  compute_view
from    wordcloud            import  WordCloud, STOPWORDS
from          PIL            import  Image
st.set_page_config(page_title='SYD', page_icon='🌃', layout='wide', initial_sidebar_state='expanded')
# DATA:
DATA         = 'dataset/SYD20230606AirBnB.csv.gz'
@st.cache_data
def load_data():
    rename   = {'name'                          :'listing',
                'host_name'                     :'host'   ,
                'room_type'                     :'room'   ,
                'minimum_nights'                :'nights' ,
                'number_of_reviews'             :'reviews',
                'availability_365'              :'365'    ,
                'number_of_reviews_ltm'         :'ltm'    } # Last Twelve Months
    data         =  pd.read_csv(DATA                      )
    data         =data.rename(columns=rename              )
# Cleaning:
    data         =data.fillna({'host' :'HOST'})
    data         =data.fillna({'last' :     0})
    data         =data.fillna({'month':     0})
    data         =data.dropna(subset=['description'], axis=0)
    data['price']=data.price.replace('[\$,]', '', regex=True).astype(float)
# OutLiers:
    data.drop(data[data['price'  ] > 600].index, axis=0, inplace=True)
    data.drop(data[data['nights' ] >  90].index, axis=0, inplace=True)
    data.drop(data[data['reviews'] >  50].index, axis=0, inplace=True)
# Selecting:
    columns  = ['listing'       ,
                'host'          ,
                'neighbourhood' ,
                'latitude'      ,
                'longitude'     ,
                'room'          ,
                'price'         ,
                'nights'        ,
                'reviews'       ,
                '365'           ,
                'ltm'           ,
                'description'   ]    
    data     = data[list(columns)]
    return     data
df           = load_data()
hood         = df.neighbourhood.unique().tolist()
room         = df.room.unique().tolist()
# SIDE:
st.sidebar.title    (  'ƊⱭȾɅViƧi🧿Ƞ&trade;')
st.sidebar.success  (  'InSide AirBnB'      )
st.sidebar.divider  (                       )
st.sidebar.header   (  'SYDNEY       '      )
st.sidebar.subheader(  'Data Analysis'      )
st.sidebar.markdown ('''Source: [InSide AirB**n**B](http://insideairbnb.com/get-the-data.html)''')
st.sidebar.write    (  'Data Base Date: 2023.06.06')
#   Maps            PlaceHolder:
st.sidebar.write('Map Options:')
InterActiveMap= st.sidebar.empty()
SimpleMap     = st.sidebar.empty()
# NeighbourHood MultiSelect:
FilteredHood  = st.sidebar.multiselect(label  = 'NeighBourHood:',
                                      options=  hood,
                                      default=['Sydney, New South Wales, Australia'])
# Room Type MultiSelect:
FilteredRoom  = st.sidebar.multiselect(label  = 'RoomType:',
                                      options=  room,
                                      default=['Entire home/apt','Private room','Shared room','Hotel room'])
# Price Slider:
FilteredPrice = st.sidebar.slider('Price:', 0.01, 599.99, 255.75, step=None)
# Filtered Data:
FilteredDF    = df[(df.neighbourhood.isin(FilteredHood)) & (df.room.isin(FilteredRoom)) & (df.price <= FilteredPrice)]
# PlaceHoder UpDate:
st.sidebar.info('{} Filtered Listings'.format(FilteredDF.shape[0]))
#   Table           PlaceHolder:
table         = st.sidebar.empty()
st.sidebar.divider(              )
st.sidebar.markdown('''
![2023.09.23   ](https://img.shields.io/badge/2023.09.23-000000)

[![License     ](https://img.shields.io/badge/Apache--2.0-D22128?&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

[![GitHub      ](https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium      ](https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn    ](https://img.shields.io/badge/in-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python      ](https://img.shields.io/badge/3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logoColor=0065FF&label=&copy;2023&labelColor=0065FF)](https://datavision.one/)
                    ''')
# MAIN:
st.divider(                    )
st.title('Inside Sydney Airbnb')
st.divider(                    )
# WordCloud:
#SYD         =  pd.read_csv('datasets/SYD20230606AirBnB.csv.gz')
#select      =['description']
#text        =  SYD[list(select)]
#description =  text.dropna(subset=['description'], axis=0)['description']
with st.spinner(text='Loading…'):#, show_time=True):
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
st.divider(                                             )
# MAPS:
if  InterActiveMap.checkbox('InterActive', value=True):
    st.subheader(           'InterActive Map')
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
    st.divider(                    )
if  SimpleMap.checkbox('Simple'):
    st.subheader(      'Simple Map')
    st.map(FilteredDF)
    st.divider(                    )
# Correlation Matrix & HeatMap:
L, R = st.columns(2)
with L:
    st.subheader('CorrelationMatrix')
    corr = FilteredDF[['price','nights','reviews']].corr().round(2)
    corr
with R:
    st.subheader(   'HeatMap')
    corr      = FilteredDF[['price','nights','reviews']].corr()
    fig2, ax2 = plt.subplots()
    ax2       = sns.heatmap(corr,
                            fmt       ='.2f',
                            cbar      = True,
                            annot     = True,
                            square    = True,
                            cmap      ='bone',
                            linewidths=      1,
                            linecolor ='white')
    st.pyplot(fig2,
              clear_figure=None,
              use_container_width=True)
st.divider(                           )
# Data Table:
if table.checkbox('DataFrame', value=True):
    st.subheader('DATA')
    st.write(    'InSide SydNey AirBnB')
    st.markdown(f'''➡️  Showing {'**{}**'.format(FilteredDF.shape[0])} **{', '.join(FilteredRoom)}** in **{', '.join(FilteredHood)}** under **AUD {FilteredPrice}**:''')
    st.write(FilteredDF)
    st.divider(        )
st.toast(        'SYD!',             icon='🌃')
