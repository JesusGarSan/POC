from streamlit_calendar import calendar
import streamlit as st
import datetime


hoy = datetime.date.today()
hoy = '2023-09-27'
import pandas as pd

df = pd.read_csv('eventos.csv', delimiter=';')


st.set_page_config(page_title="Calendario", page_icon="📆", layout='wide')




with st.expander('df de eventos:'):
    edited_df = st.data_editor(df)
    if st.button('sobreescribir .csv'):
        print('guardando')
        edited_df.to_csv('eventos.csv', sep=';', index=False)
        print('guardado')



eventos = edited_df.to_dict(orient='records')


mode = st.selectbox(
    "Modo de representación:", ("timegrid", "daygrid", "timeline",
                       "resource-daygrid", "resource-timegrid", "resource-timeline",
                       "list", "multimonth")
)

calendar_options = {}
calendar_events = eventos

calendar_resources = [
    {'id': 'casa', 'building': 'Casa', 'title': 'Casa'},
    {'id': 'ofi', 'building': 'Oficina', 'title': 'Oficina'},
    {'id': 'uni', 'building': 'Facultad', 'title': 'Facultad'},
]

if ("resource" in mode):
    if (mode == "resource-daygrid"):
        calendar_options = {
            'navLinks': 'true',
            'initialDate': f"{hoy}",
            'initialView': 'resourceDayGridDay',
            'resourceGroupField': 'building',
            'resources': calendar_resources,
            'locale': 'es',
            'firstDay': 1,
        }
    elif (mode == "resource-timeline"):
        calendar_options = {
            'headerToolbar': {
                'left': 'today prev,next',
                'center': 'title',
                'right': 'resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth'
            },
            'businessHours':{
                'daysOfWeek': [1,2,3,4,5],
                'startTime': '07:00',
                'endTime': '15:00',
                'timeFormat': 'HH:mm',

            },
            'navLinks': 'true',
            'initialDate': f"{hoy}",
            'initialView': 'resourceTimelineDay',
            'resourceGroupField': 'building',
            'resources': calendar_resources,
            'locale': 'es',
            'firstDay': 1,
        }
    elif (mode == "resource-timegrid"):
        calendar_options = {
            'navLinks': 'true',
            'initialDate': f"{hoy}",
            'initialView': 'resourceTimeGridDay',
            'resourceGroupField': 'building',
            'resources': calendar_resources,
            'locale': 'es',
            'firstDay': 1,
            'businessHours':{
                'daysOfWeek': [1,2,3,4,5],
                'startTime': '07:00',
                'endTime': '15:00',
                'timeFormat': 'HH:mm',

            },
        }
else:
    if (mode == "daygrid"):
        calendar_options = {
            'headerToolbar': {
                'left': 'today prev,next',
                'center': 'title',
                'right': 'dayGridDay,dayGridWeek,dayGridMonth'
            },
            'navLinks': 'true',
            'initialDate': f"{hoy}",
            'initialView': 'dayGridMonth',
            'locale': 'es',
            'firstDay': 1,
            'businessHours':{
                'daysOfWeek': [1,2,3,4,5],
                'startTime': '07:00',
                'endTime': '15:00',
                'timeFormat': 'HH:mm',

            },
        }
    elif (mode == "timegrid"):
        calendar_options = {
            'navLinks': 'true',
            'initialView': 'timeGridWeek',
            'locale': 'es',
            'firstDay': 1,
            'businessHours':{
                'daysOfWeek': [1,2,3,4,5],
                'startTime': '07:00',
                'endTime': '15:00',
                'timeFormat': 'HH:mm',

            },
        }
    elif (mode == "timeline"):
        calendar_options = {
            'headerToolbar': {
                'left': 'today prev,next',
                'center': 'title',
                'right': 'timelineDay,timelineWeek,timelineMonth'
            },
            'navLinks': 'true',
            'initialDate': f"{hoy}",
            'initialView': 'timelineMonth',
            'locale': 'es',
            'firstDay': 1,
            'businessHours':{
                'daysOfWeek': [1,2,3,4,5],
                'startTime': '07:00',
                'endTime': '15:00',
                'timeFormat': 'HH:mm',

            },
        }
    elif (mode == "list"):
        calendar_options = {
            'navLinks': 'true',
            'initialDate': f"{hoy}",
            'initialView': 'listMonth',
            'locale': 'es',
            'firstDay': 1,
            'businessHours':{
                'daysOfWeek': [1,2,3,4,5],
                'startTime': '07:00',
                'endTime': '15:00',
                'timeFormat': 'HH:mm',

            },
        }
    elif (mode == "multimonth"):
        calendar_options = {
            'navLinks': 'true',
            'initialView': 'multiMonthYear',
            'locale': 'es',
            'firstDay': 1,
            'businessHours':{
                'daysOfWeek': [1,2,3,4,5],
                'startTime': '07:00',
                'endTime': '15:00',
                'timeFormat': 'HH:mm',

            },
        }


state = calendar(events=calendar_events, options=calendar_options, key=mode,)

#st.write(state)

st.markdown("## API reference")
st.help(calendar)