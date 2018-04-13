import sqlite3
import json


class Report(object):
    """
    A pathology report of an anonymized patient. Reports have the following properties:

    Attributes:
        patient_ID: The anonymized ID of the pateint's report
        cancer_site: The site of the cancer e.g. lung, colon, skin
        diabetes_status: The diabetes states of the patient e.g. Type 1, Type 2, Positive (unk), Negative
        surgery_type: The type of surgery done on the patient e.g. pancreatectomy, whipple
        tabular_results: List of any results in a data table (JSON format)
        measurements: Any measurements taken of the patient (JSON format)
        medications: Any medications prescribed to the patient (JSON format)
    """

    def __init__(self, patient_ID, cancer_site=None, diabetes_status=None, surgery_type=None, tabular_results=None, measurements=None, medications=None):
        """
        Return a Report object with default values as None
        """
        self.patient_ID = patient_ID
        self.cancer_site = cancer_site
        self.diabetes_status = diabetes_status
        self.surgery_type = surgery_type
        self.tabular_results = tabular_results
        self.measurements = measurements
        self.medications = medications

    def save(pathname):
        """
        Save a Report class to the local sqlite3 database located at the pathname
        """
        try:
            db = sqlite3.connect(pathname)  # data/mydb
            cursor = db.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients(
                    patient_ID TEXT PRIMARY KEY UNIQUE NOT NULL,
                    cancer_site TEXT NULL,
                    diabetes_status TEXT NULL,
                    surgery_type TEXT NULL,
                    tabular_results json NULL,
                    measurements json NULL,
                    medications json NULL)''')
            db.commit()

            cursor.execute('''
                INSERT INTO patients(
                    patient_ID,
                    cancer_site,
                    diabetes_status,
                    surgery_type,
                    tabular_results,
                    measurements,
                    medications)
                VALUES(?,?,?,?,?,?,?)
                ''', (self.patient_ID,
                      self.cancer_site,
                      self.diabetes_status,
                      self.surgery_type,
                      self.tabular_results,
                      self.measurements,
                      self.medications,))
            db.commit()

        except Exception as e:
            db.rollback()
            raise e

        finally:
            db.close()

        return True

    def load(pathname):
        try:
            db = sqlite3.connect(pathname)  # data/mydb
            cursor = db.cursor()

            cursor.execute('''
                SELECT cancer_site, diabetes_status, surgery_type, tabular_results, measurements, medications
                FROM patients WHERE patient_ID=?
                ''', (self.patient_ID,))

        except Exception as e:
            db.rollback()
            raise e

        finally:
            db.close()

        return True
