import streamlit as st
from streamlit_lottie import st_lottie
import requests
from datetime import date, datetime, time, timedelta
from sign_in_page import sign_in_page
from sign_up_page import sign_up_page


FEATURE_PAGES = [
    ("Dashboard", "home"),
    ("Memos", "memos"),
    ("Chat", "chat"),
    ("Calendar", "calendar"),
    ("Organize", "organize"),
]


def ensure_session_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def require_sign_in() -> bool:
    if not st.session_state.get("signed_in"):
        st.info("Please sign in to access this workspace.")
        return False
    return True

# Function to load a Lottie animation from a URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Function for the sidebar buttons and dropdown
def sidebar():
    # Full-width button styling for sidebar
    st.markdown(""" 
        <style> 
        .css-1cpxqw2 { width: 100% !important; }  
        .stButton button { width: 100% !important; }  
        .stSelectbox, .stRadio { width: 100% !important; }  
        .css-1d391kg {
            background-color: #f5f5f5 !important;
            padding: 1em;
        }
        </style>
    """, unsafe_allow_html=True)

    feature_labels = [item[0] for item in FEATURE_PAGES]
    feature_lookup = {label: page_key for label, page_key in FEATURE_PAGES}
    current_page = st.session_state.get("page", "home")
    current_label = next((label for label, key in FEATURE_PAGES if key == current_page), feature_labels[0])

    with st.sidebar:
        home_button = st.button("Dashboard", key="home_sidebar_1")

        selected_label = st.selectbox(
            "Workspace",
            feature_labels,
            index=feature_labels.index(current_label),
            key="features_sidebar_1",
        )

        # Check if signed in
        if st.session_state.get("signed_in", False):
            sign_out_button = st.button("Sign Out", key="sign_out_button_1")
            return home_button, feature_lookup[selected_label], None, None, sign_out_button
        else:
            sign_in_button = st.button("Sign In", key="sign_in_button_1")
            sign_up_button = st.button("Sign Up", key="sign_up_button_1")
            return home_button, feature_lookup[selected_label], sign_in_button, sign_up_button, None




# Title page with typing animation and button
def title_page():
    # Typing animation and blinking cursor CSS
    st.markdown("""
        <style>
        .typewriter h1 {
            overflow: hidden; 
            border-right: .15em solid orange; 
            white-space: nowrap; 
            margin: 0 auto; 
            letter-spacing: .15em;
            animation: 
                typing 2.5s steps(30, end),
                blink-caret .75s step-end infinite;
            font-size: 60px;
            text-align: center;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: orange; }
        }

        /* Hide button initially */
        #continue-btn {
            display: none;
            text-align: center;
        }

        /* Make button full width */
        #continue-btn button {
            width: 100%;
            font-size: 18px;
            padding: 0.5em 1em;
        }
        </style>

        <div class="typewriter">
            <h1>Personal Assistant</h1>
        </div>
    """, unsafe_allow_html=True)

    # JS to reveal button after animation
    st.markdown("""
        <script>
            setTimeout(() => {
                const btn = window.parent.document.querySelector('[data-testid="stButton"]');
                if (btn) {
                    const wrapper = document.getElementById("continue-btn");
                    if (wrapper) {
                        wrapper.style.display = "block";
                    }
                }
            }, 2700);
        </script>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Centered button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
                <style>
                    div.stButton > button {
                        width: 100%;
                    }
                </style>
            """, unsafe_allow_html=True)

        if st.button("Continue to app >>"):
            st.session_state.page = "home"

        st.markdown('</div>', unsafe_allow_html=True)

def home_page():
    if st.session_state.get("signed_in"):
        st.title("Welcome to Your Dashboard")
        st.caption("Quick links to your workspace")

        feature_cols = st.columns(2)
        feature_buttons = FEATURE_PAGES[1:]
        should_rerun = False

        for idx, (label, page_key) in enumerate(feature_buttons):
            col = feature_cols[idx % 2]
            with col:
                if st.button(label, key=f"home_{page_key}"):
                    st.session_state.page = page_key
                    should_rerun = True

        if should_rerun:
            st.rerun()

        st.divider()

        upcoming_events = st.session_state.get("calendar_events", [])
        tasks = st.session_state.get("organize_tasks", [])
        memos = st.session_state.get("memos", [])

        st.subheader("Today at a glance")
        if upcoming_events:
            st.markdown(
                "- **Next event:** {} on {}".format(
                    upcoming_events[0]["title"],
                    upcoming_events[0]["datetime"].strftime("%b %d, %I:%M %p"),
                )
            )
        else:
            st.markdown("- No events scheduled yet. Head to `Calendar` to add one.")

        if tasks:
            remaining = [task for task in tasks if not task["completed"]]
            st.markdown(f"- **Tasks remaining:** {len(remaining)}")
        else:
            st.markdown("- Start organizing your tasks from the `Organize` tab.")

        if memos:
            st.markdown(f"- **Latest memo:** {memos[-1]['title']}")
        else:
            st.markdown("- Capture quick thoughts in the `Memos` workspace.")
    else:
        st.title("Welcome to Our AI-Powered Personal Assistant!")
        st.write(
            """
            Our app is a personal assistant powered by AI.
            It will help you set reminders, keep track of important dates, and more.
            You can use it to manage your calendar, create tasks, and get notifications.
            Stay organized and on top of your schedule!
            """
        )
        lottie_url = "https://assets1.lottiefiles.com/packages/lf20_mjlh3hcy.json"
        lottie_json = load_lottie_url(lottie_url)

        if lottie_json:
            st_lottie(lottie_json, speed=1, height=300, key="ai_lottie")


def generate_chat_response(message: str) -> str:
    lowered = message.lower()
    memos = st.session_state.get("memos", [])
    tasks = st.session_state.get("organize_tasks", [])
    events = st.session_state.get("calendar_events", [])

    def summarize_events(event_list, max_items=3):
        if not event_list:
            return "You don't have any events scheduled yet."
        parts = []
        for event in event_list[:max_items]:
            dt = event["datetime"]
            parts.append(f"{dt.strftime('%a %b %d at %I:%M %p')} — {event['title']}")
        if len(event_list) > max_items:
            parts.append(f"…and {len(event_list) - max_items} more events.")
        return "\n".join(parts)

    def summarize_tasks(task_list, only_open=False):
        if not task_list:
            return "You're task-free right now."
        filtered = [task for task in task_list if not task["completed"]] if only_open else task_list
        if not filtered:
            return "All of your tasks are checked off. Nice work!"
        parts = []
        for task in filtered[:3]:
            status = "done" if task["completed"] else task["priority"].lower()
            parts.append(f"{task['title']} ({status})")
        if len(filtered) > 3:
            parts.append(f"…and {len(filtered) - 3} more tasks.")
        return "\n".join(parts)

    if "help" in lowered or "what can" in lowered:
        return (
            "Ask me about your memos, calendar, or tasks — for example: "
            "'show my calendar for tomorrow', 'summarize my tasks', or 'latest memo'."
        )

    if "memo" in lowered:
        if memos:
            latest = memos[-1]
            body = latest["body"] or "(no extra details)"
            return f"Your latest memo '{latest['title']}' says: {body}"
        return "You don't have any memos yet. Capture a new one in the Memos tab."

    if any(keyword in lowered for keyword in ["task", "todo", "to-do", "organize", "priority"]):
        return "Here are the tasks on your radar:\n" + summarize_tasks(tasks, only_open=True)

    if any(keyword in lowered for keyword in ["calendar", "schedule", "event", "meeting", "plan"]):
        if "weekend" in lowered:
            today = datetime.now().date()
            days_until_saturday = (5 - today.weekday()) % 7
            saturday = today + timedelta(days=days_until_saturday)
            sunday = saturday + timedelta(days=1)
            weekend_events = [
                event for event in events
                if saturday <= event["datetime"].date() <= sunday
            ]
            if weekend_events:
                return "Here's what's on your weekend agenda:\n" + summarize_events(weekend_events)
            return "Your weekend is wide open. Add plans in the Calendar tab when you're ready."

        if "tomorrow" in lowered:
            tomorrow = datetime.now().date() + timedelta(days=1)
            tomorrow_events = [event for event in events if event["datetime"].date() == tomorrow]
            if tomorrow_events:
                return "Tomorrow you have:\n" + summarize_events(tomorrow_events)
            return "No events tomorrow."

        if "today" in lowered:
            today = datetime.now().date()
            today_events = [event for event in events if event["datetime"].date() == today]
            if today_events:
                return "Today's schedule:\n" + summarize_events(today_events)
            return "Nothing on the calendar for today."

        return "Upcoming events:\n" + summarize_events(events)

    if "weekend" in lowered and "plan" in lowered:
        if events:
            response_lines = ["Let's plan your weekend:"]
            response_lines.append("Calendar:")
            response_lines.append(summarize_events(events))
            open_tasks = summarize_tasks(tasks, only_open=True)
            if open_tasks:
                response_lines.append("Tasks to wrap up:")
                response_lines.append(open_tasks)
            if memos:
                response_lines.append("Recent memo inspiration:")
                response_lines.append(f"- {memos[-1]['title']}")
            return "\n".join(response_lines)
        return "Your weekend is open. Add events in Calendar or notes in Memos to build a plan."

    if "memos" in lowered or "notes" in lowered and memos:
        titles = ", ".join(memo["title"] for memo in memos[-3:])
        return f"Your recent memos: {titles}."

    if "status" in lowered or "summary" in lowered or "overview" in lowered:
        parts = ["Here's your workspace summary:"]
        parts.append("Calendar:")
        parts.append(summarize_events(events))
        parts.append("Tasks:")
        parts.append(summarize_tasks(tasks, only_open=True))
        if memos:
            parts.append("Latest memo:")
            parts.append(f"{memos[-1]['title']} — {memos[-1]['body'] or '(no details)'}")
        else:
            parts.append("No memos yet.")
        return "\n".join(parts)

    return (
        "I'm here to keep you organized. Try asking about your calendar, tasks, memos, or say 'help' for ideas."
    )


def memos_page():
    if not require_sign_in():
        return

    st.title("Memos")
    st.caption("Capture quick notes and ideas.")

    memos = ensure_session_state("memos", [])

    with st.form("memo_form"):
        title = st.text_input("Title", placeholder="Weekly planning notes")
        body = st.text_area("Memo", height=150)
        submitted = st.form_submit_button("Save memo")

        if submitted:
            if not title.strip() and not body.strip():
                st.warning("Add a title or memo text before saving.")
            else:
                memos.append(
                    {
                        "title": title.strip() or "Untitled memo",
                        "body": body.strip(),
                        "created": datetime.now(),
                    }
                )
                st.session_state.memos = memos
                st.success("Memo saved!")
                st.rerun()

    if memos:
        st.subheader("Recent memos")
        for idx in range(len(memos) - 1, -1, -1):
            memo = memos[idx]
            header = f"{memo['title']} · {memo['created'].strftime('%b %d %Y, %I:%M %p')}"
            with st.expander(header, expanded=idx == len(memos) - 1):
                st.write(memo["body"] or "_No additional notes._")
                if st.button("Delete", key=f"delete_memo_{idx}"):
                    memos.pop(idx)
                    st.session_state.memos = memos
                    st.success("Memo removed")
                    st.rerun()
    else:
        st.info("No memos yet. Use the form above to add your first memo.")


def chat_page():
    if not require_sign_in():
        return

    st.title("Chat Companion")
    st.caption("Get quick summaries of your workspace.")

    history = ensure_session_state("chat_history", [])

    for message in history:
        st.chat_message(message["role"]).write(message["content"])

    prompt = st.chat_input("Ask me about your plans...")

    if prompt:
        history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = generate_chat_response(prompt)
        history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

        st.session_state.chat_history = history


def calendar_page():
    if not require_sign_in():
        return

    st.title("Calendar")
    st.caption("Plan upcoming events and milestones.")

    events = ensure_session_state("calendar_events", [])

    with st.form("calendar_form"):
        event_date = st.date_input("Date", value=date.today())
        event_time = st.time_input("Time", value=time(9, 0))
        title = st.text_input("Event title", placeholder="Team sync")
        notes = st.text_area("Notes", placeholder="Agenda or reminders", height=100)
        submitted = st.form_submit_button("Add event")

        if submitted:
            if not title.strip():
                st.warning("Please provide a title for the event.")
            else:
                events.append(
                    {
                        "title": title.strip(),
                        "datetime": datetime.combine(event_date, event_time),
                        "notes": notes.strip(),
                    }
                )
                events.sort(key=lambda item: item["datetime"])
                st.session_state.calendar_events = events
                st.success("Event added")
                st.rerun()

    if events:
        st.subheader("Upcoming schedule")
        for idx, event in enumerate(events):
            st.markdown(
                "**{}** — {}".format(
                    event["title"], event["datetime"].strftime("%b %d, %I:%M %p"),
                )
            )
            if event["notes"]:
                st.caption(event["notes"])
            if st.button("Remove", key=f"remove_event_{idx}"):
                events.pop(idx)
                st.session_state.calendar_events = events
                st.success("Event removed")
                st.rerun()
    else:
        st.info("No events scheduled yet. Add your first event above.")


def organize_page():
    if not require_sign_in():
        return

    st.title("Organize")
    st.caption("Track tasks and priorities.")

    tasks = ensure_session_state("organize_tasks", [])

    with st.form("task_form"):
        title = st.text_input("Task", placeholder="Prepare project report")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
        submitted = st.form_submit_button("Add task")

        if submitted:
            if not title.strip():
                st.warning("Enter a task description before adding.")
            else:
                tasks.append(
                    {
                        "title": title.strip(),
                        "priority": priority,
                        "completed": False,
                    }
                )
                st.session_state.organize_tasks = tasks
                st.success("Task added")
                st.rerun()

    if tasks:
        st.subheader("Your tasks")
        for idx, task in enumerate(tasks):
            cols = st.columns([0.1, 0.6, 0.2, 0.1])
            completed = cols[0].checkbox("", value=task["completed"], key=f"task_done_{idx}")
            if completed != task["completed"]:
                tasks[idx]["completed"] = completed
                st.session_state.organize_tasks = tasks

            cols[1].write(task["title"])
            cols[2].write(f"Priority: {task['priority']}")
            if cols[3].button("✕", key=f"delete_task_{idx}"):
                tasks.pop(idx)
                st.session_state.organize_tasks = tasks
                st.success("Task removed")
                st.rerun()

        completed_count = sum(1 for task in tasks if task["completed"])
        st.caption(f"{completed_count} of {len(tasks)} tasks completed")
    else:
        st.info("No tasks yet. Use the form above to add your first task.")


# Main function to handle page navigation
def main():
    if "page" not in st.session_state:
        st.session_state.page = "title"
    if "signed_in" not in st.session_state:
        st.session_state.signed_in = False

    # Page routing logic
    if st.session_state.page == "title":
        title_page()
    else:
        # Call sidebar AFTER state updates
        home_button, feature_selection, sign_in_button, sign_up_button, sign_out_button = sidebar()

        # Handle navigation buttons
        if sign_in_button:
            st.session_state.page = "sign_in"
        elif sign_up_button:
            st.session_state.page = "sign_up"
        elif sign_out_button:
            st.session_state.signed_in = False
            st.session_state.page = "home"
        elif home_button:
            st.session_state.page = "home"

        # React to workspace selector (avoid overwriting auth pages)
        if st.session_state.page not in {"sign_in", "sign_up"} and feature_selection != st.session_state.page:
            st.session_state.page = feature_selection

        # Route to the appropriate page
        if st.session_state.page == "home":
            home_page()
        elif st.session_state.page == "memos":
            memos_page()
        elif st.session_state.page == "chat":
            chat_page()
        elif st.session_state.page == "calendar":
            calendar_page()
        elif st.session_state.page == "organize":
            organize_page()
        elif st.session_state.page == "sign_in":
            sign_in_page()
        elif st.session_state.page == "sign_up":
            sign_up_page()


if __name__ == "__main__":
    main()
