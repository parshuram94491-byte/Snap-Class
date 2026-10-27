import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    style_background_home()
    style_base_layout()
    st.markdown('<div class="snap-home-page" aria-hidden="true">&#8203;</div>', unsafe_allow_html=True)
    header_home()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="portal-card student-card">
                <div class="card-inner-content">
                    <div class="card-text-col">
                        <div class="card-role-im">I'm</div>
                        <div class="card-role-title role-student">Student</div>
                        <p class="card-desc">Access your classes, view attendance and stay updated.</p>
                    </div>
                    <div class="card-mascot-box">
                        <svg class="mascot-sparks student-sparks" viewBox="0 0 40 24" fill="none">
                            <line x1="8" y1="20" x2="2" y2="8" stroke="#3B82F6" stroke-width="2.8" stroke-linecap="round"/>
                            <line x1="20" y1="18" x2="20" y2="4" stroke="#3B82F6" stroke-width="2.8" stroke-linecap="round"/>
                            <line x1="32" y1="20" x2="38" y2="8" stroke="#3B82F6" stroke-width="2.8" stroke-linecap="round"/>
                        </svg>
                        <svg class="mascot-img student-mascot" viewBox="0 0 220 260" role="img" aria-label="Student holding a book" preserveAspectRatio="xMidYMax meet">
                            <ellipse cx="113" cy="246" rx="82" ry="10" fill="#DCE8FF"/>
                            <path d="M38 244c3-51 13-84 47-99h56c35 14 43 48 47 99H38Z" fill="#3267F5"/>
                            <path d="M77 150c3 23 14 35 36 35s34-12 37-35l-20-15H96l-19 15Z" fill="#F2B69B"/>
                            <path d="M84 153c7 12 17 18 29 18s24-7 32-19l-15-13H98l-14 14Z" fill="#fff"/>
                            <path d="M78 82c0-34 18-55 43-55 27 0 46 23 44 58l-8 39c-7 22-24 34-40 34-20 0-35-16-40-39l1-37Z" fill="#F7C6A7"/>
                            <path d="M77 91c-10-28-1-60 21-70 24-12 59-4 69 25 4 11 2 25-2 34-3-15-13-25-24-31-15 17-39 22-62 17l-2 25Z" fill="#202C66"/>
                            <path d="M83 69c13-2 29-7 42-16 7 12 21 18 36 19" fill="none" stroke="#354889" stroke-width="9" stroke-linecap="round"/>
                            <circle cx="104" cy="105" r="4" fill="#1E315F"/>
                            <circle cx="139" cy="105" r="4" fill="#1E315F"/>
                            <path d="M111 126c8 7 17 7 24 0" fill="none" stroke="#C45C67" stroke-width="3" stroke-linecap="round"/>
                            <path d="M63 190c11-14 24-19 39-17l19 11 20-11c14 0 26 6 36 19l10 52H51l12-54Z" fill="#3474FF"/>
                            <path d="M98 177h27l12 67H88l10-67Z" fill="#fff"/>
                            <path d="M113 185v58" stroke="#E4EBFA" stroke-width="3"/>
                            <path d="M79 204 57 225l18 14 25-24m42-10 23 20-17 15-26-23" fill="#F2B69B"/>
                            <path d="M74 206 47 226l21 21 30-22-11-18-13-1Zm77-1 27 19-17 23-32-20 10-19 12-3Z" fill="#1F53D6"/>
                            <path d="M81 202 133 188c4-1 8 1 9 5l13 39c1 4-1 8-5 9l-51 14-18-47Z" fill="#1652B9" stroke="#103C91" stroke-width="3"/>
                            <path d="M81 202 103 251" stroke="#7BB5FF" stroke-width="3"/>
                            <path d="m105 211 27-7m-22 17 26-7" stroke="#A8D4FF" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button('Student Portal ↗', key='btn_student_portal', use_container_width=True):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="portal-card teacher-card">
                <div class="card-inner-content">
                    <div class="card-text-col">
                        <div class="card-role-im">I'm</div>
                        <div class="card-role-title role-teacher">Teacher</div>
                        <p class="card-desc">Take attendance, manage subjects and track records.</p>
                    </div>
                    <div class="card-mascot-box">
                        <svg class="mascot-sparks teacher-sparks" viewBox="0 0 40 24" fill="none">
                            <line x1="8" y1="20" x2="2" y2="8" stroke="#EC4899" stroke-width="2.8" stroke-linecap="round"/>
                            <line x1="20" y1="18" x2="20" y2="4" stroke="#EC4899" stroke-width="2.8" stroke-linecap="round"/>
                            <line x1="32" y1="20" x2="38" y2="8" stroke="#EC4899" stroke-width="2.8" stroke-linecap="round"/>
                        </svg>
                        <svg class="mascot-img teacher-mascot" viewBox="0 0 220 260" role="img" aria-label="Teacher with a book and magnifying glass" preserveAspectRatio="xMidYMax meet">
                            <ellipse cx="111" cy="246" rx="83" ry="10" fill="#F8DDEB"/>
                            <path d="M35 244c4-52 15-84 49-99h56c35 14 45 47 48 99H35Z" fill="#EC4B9D"/>
                            <path d="M78 151c4 22 14 34 35 34 22 0 34-13 37-35l-20-14H98l-20 15Z" fill="#E8A98D"/>
                            <path d="m91 144 22 23 23-23 13 13-21 34H98l-20-33 13-14Z" fill="#fff"/>
                            <path d="M78 82c0-34 18-55 43-55 27 0 46 23 44 58l-8 39c-7 22-24 34-40 34-20 0-35-16-40-39l1-37Z" fill="#F4B99A"/>
                            <path d="M77 91c-10-28-1-60 21-70 24-12 59-4 69 25 4 11 2 25-2 34-3-15-13-25-24-31-15 17-39 22-62 17l-2 25Z" fill="#29264E"/>
                            <path d="M83 69c13-2 29-7 42-16 7 12 21 18 36 19" fill="none" stroke="#45406D" stroke-width="9" stroke-linecap="round"/>
                            <circle cx="104" cy="106" r="4" fill="#252A51"/>
                            <circle cx="139" cy="106" r="4" fill="#252A51"/>
                            <path d="M111 126c8 7 17 7 24 0" fill="none" stroke="#B65365" stroke-width="3" stroke-linecap="round"/>
                            <path d="M61 191c11-14 24-19 39-17l13 13 15-13c15 0 28 7 37 20l9 50H50l11-53Z" fill="#EF4D9E"/>
                            <path d="m101 183 12 7 12-7 7 61h-39l8-61Z" fill="#fff"/>
                            <path d="M111 192v52" stroke="#E5E7EB" stroke-width="3"/>
                            <path d="m107 193 5 7 6-7-6 28-5-28Z" fill="#253F8A"/>
                            <path d="M66 207 48 225l20 19 29-21-11-18-20 2Z" fill="#F4B99A"/>
                            <path d="m68 205 23-7 11 20-30 20-16-17 12-16Z" fill="#164EB7"/>
                            <path d="M146 207 163 222l-13 20-27-20 10-18 13 3Z" fill="#F4B99A"/>
                            <path d="M80 203 116 214v31H84l-13-25 9-17Z" fill="#1652B9" stroke="#103C91" stroke-width="3"/>
                            <path d="m85 211 23 7m-18 3 19 6" stroke="#A8D4FF" stroke-width="2" stroke-linecap="round"/>
                            <circle cx="171" cy="124" r="24" fill="none" stroke="#253F8A" stroke-width="7"/>
                            <circle cx="171" cy="124" r="17" fill="#E9F3FF" fill-opacity=".72"/>
                            <path d="m187 142 19 20" stroke="#253F8A" stroke-width="8" stroke-linecap="round"/>
                        </svg>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button('Teacher Portal ↗', key='btn_teacher_portal', use_container_width=True):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()
