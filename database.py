import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path='instance/sptws.db'):
        instance_dir = os.path.dirname(db_path)
        if instance_dir and not os.path.exists(instance_dir):
            os.makedirs(instance_dir)
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                event_date DATE,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Committee members
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS committee_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT,
                bio TEXT,
                phone TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Society members
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS society_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                designation TEXT,
                school TEXT,
                phone TEXT,
                email TEXT,
                joined_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        # Annual reports
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS annual_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                file_path TEXT NOT NULL,
                year INTEGER,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Gallery
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gallery (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                caption TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Software links
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS software_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Important GOs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS important_gos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                go_number TEXT,
                file_path TEXT NOT NULL,
                description TEXT,
                issued_date DATE,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        self.add_sample_data()
    
    def add_sample_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        if cursor.fetchone()[0] == 0:
            sample_events = [
                ("Annual Teachers' Training Workshop", "Professional development workshop for teachers", "2024-03-15", "Sircilla Town Hall"),
                ("Science Exhibition", "Inter-school science exhibition", "2024-02-20", "Government High School, Sircilla"),
                ("Parent-Teacher Meet", "Annual parent-teacher interaction program", "2024-01-10", "Zilla Parishad High School"),
            ]
            cursor.executemany("INSERT INTO events (title, description, event_date, location) VALUES (?, ?, ?, ?)", sample_events)
            
            sample_committee = [
                ("Dr. K. Rajesh", "President", "20+ years of teaching experience", "9876543210", "president@sptws.org"),
                ("M. Sunitha", "Secretary", "Education reform advocate", "9876543211", "secretary@sptws.org"),
                ("P. Venkatesh", "Treasurer", "Financial expert", "9876543212", "treasurer@sptws.org"),
            ]
            cursor.executemany("INSERT INTO committee_members (name, position, bio, phone, email) VALUES (?, ?, ?, ?, ?)", sample_committee)
            
            sample_members = [
                ("R. Narsimha", "Senior Teacher", "ZPHS Sircilla", "9988776655", "narsimha@email.com"),
                ("S. Laxmi", "Head Master", "GPS Sircilla", "9988776644", "laxmi@email.com"),
                ("T. Srinivas", "Science Teacher", "MPUPS Sircilla", "9988776633", "srinivas@email.com"),
            ]
            cursor.executemany("INSERT INTO society_members (name, designation, school, phone, email) VALUES (?, ?, ?, ?, ?)", sample_members)
            
            sample_links = [
                ("DIKSHA Platform", "National teachers' platform for learning resources", "https://diksha.gov.in"),
                ("SWAYAM", "Free online courses for teachers", "https://swayam.gov.in"),
                ("NCERT Books", "Free NCERT textbooks and resources", "https://ncert.nic.in"),
            ]
            cursor.executemany("INSERT INTO software_links (title, description, url) VALUES (?, ?, ?)", sample_links)
        conn.commit()
        conn.close()
    
    # ---------- Event methods ----------
    def get_all_events(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events ORDER BY event_date DESC")
        events = cursor.fetchall()
        conn.close()
        return events
    
    def get_recent_events(self, limit=3):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events ORDER BY event_date DESC LIMIT ?", (limit,))
        events = cursor.fetchall()
        conn.close()
        return events
    
    def add_event(self, title, description, event_date, location):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (title, description, event_date, location) VALUES (?, ?, ?, ?)",
                      (title, description, event_date, location))
        conn.commit()
        conn.close()
    
    def update_event(self, event_id, title, description, event_date, location):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE events SET title=?, description=?, event_date=?, location=? WHERE id=?",
                      (title, description, event_date, location, event_id))
        conn.commit()
        conn.close()
    
    def delete_event(self, event_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
        conn.close()
    
    # ---------- Committee members ----------
    def get_committee_members(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM committee_members ORDER BY position")
        members = cursor.fetchall()
        conn.close()
        return members
    
    def add_committee_member(self, name, position, bio, phone, email):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO committee_members (name, position, bio, phone, email) VALUES (?, ?, ?, ?, ?)",
                      (name, position, bio, phone, email))
        conn.commit()
        conn.close()
    
    def update_committee_member(self, member_id, name, position, bio, phone, email):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE committee_members SET name=?, position=?, bio=?, phone=?, email=? WHERE id=?",
                      (name, position, bio, phone, email, member_id))
        conn.commit()
        conn.close()
    
    def delete_committee_member(self, member_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM committee_members WHERE id = ?", (member_id,))
        conn.commit()
        conn.close()
    
    # ---------- Society members ----------
    def get_society_members(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM society_members ORDER BY name")
        members = cursor.fetchall()
        conn.close()
        return members
    
    def add_society_member(self, name, designation, school, phone, email):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO society_members (name, designation, school, phone, email) VALUES (?, ?, ?, ?, ?)",
                      (name, designation, school, phone, email))
        conn.commit()
        conn.close()
    
    def update_society_member(self, member_id, name, designation, school, phone, email):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE society_members SET name=?, designation=?, school=?, phone=?, email=? WHERE id=?",
                      (name, designation, school, phone, email, member_id))
        conn.commit()
        conn.close()
    
    def delete_society_member(self, member_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM society_members WHERE id = ?", (member_id,))
        conn.commit()
        conn.close()
    
    # ---------- Annual reports ----------
    def get_annual_reports(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM annual_reports ORDER BY year DESC")
        reports = cursor.fetchall()
        conn.close()
        return reports
    
    def add_annual_report(self, title, file_path, year):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO annual_reports (title, file_path, year) VALUES (?, ?, ?)",
                      (title, file_path, year))
        conn.commit()
        conn.close()
    
    def get_annual_report_by_id(self, report_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM annual_reports WHERE id = ?", (report_id,))
        report = cursor.fetchone()
        conn.close()
        return report
    
    def delete_annual_report(self, report_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM annual_reports WHERE id = ?", (report_id,))
        conn.commit()
        conn.close()
    
    # ---------- Gallery ----------
    def get_gallery_images(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gallery ORDER BY uploaded_at DESC")
        images = cursor.fetchall()
        conn.close()
        return images
    
    def add_gallery_image(self, image_path, caption):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO gallery (image_path, caption) VALUES (?, ?)",
                      (image_path, caption))
        conn.commit()
        conn.close()
    
    def get_gallery_image_by_id(self, image_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gallery WHERE id = ?", (image_id,))
        image = cursor.fetchone()
        conn.close()
        return image
    
    def delete_gallery_image(self, image_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gallery WHERE id = ?", (image_id,))
        conn.commit()
        conn.close()
    
    # ---------- Software links ----------
    def get_software_links(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM software_links ORDER BY title")
        links = cursor.fetchall()
        conn.close()
        return links
    
    def add_software_link(self, title, description, url):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO software_links (title, description, url) VALUES (?, ?, ?)",
                      (title, description, url))
        conn.commit()
        conn.close()
    
    def update_software_link(self, link_id, title, description, url):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE software_links SET title=?, description=?, url=? WHERE id=?",
                      (title, description, url, link_id))
        conn.commit()
        conn.close()
    
    def delete_software_link(self, link_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM software_links WHERE id = ?", (link_id,))
        conn.commit()
        conn.close()
    
    # ---------- Important GOs ----------
    def get_important_gos(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM important_gos ORDER BY uploaded_at DESC")
        gos = cursor.fetchall()
        conn.close()
        return gos
    
    def add_important_go(self, title, go_number, file_path, description):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO important_gos (title, go_number, file_path, description) VALUES (?, ?, ?, ?)",
                      (title, go_number, file_path, description))
        conn.commit()
        conn.close()
    
    def get_important_go_by_id(self, go_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM important_gos WHERE id = ?", (go_id,))
        go = cursor.fetchone()
        conn.close()
        return go
    
    def delete_important_go(self, go_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM important_gos WHERE id = ?", (go_id,))
        conn.commit()
        conn.close()