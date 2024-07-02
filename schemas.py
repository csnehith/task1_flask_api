"""Schemas"""

schema_student_details = {
    "type": "object",
    "properties": {
        "student_id": {"type": "string"},
        "school": {"type": "string"},
        "sex": {"type": "string"},
        "age": {"type": "string"},
        "address_type": {"type": "string"},
        "family_size": {"type": "string"},
        "parent_status": {"type": "string"},
        "mother_education": {"type": "string"},
        "father_education": {"type": "string"},
        "mother_job": {"type": "string"},
        "father_job": {"type": "string"},
        "school_choice_reason": {"type": "string"},
        "gaurdian": {"type": "string"},
        "travel_time": {"type": "string"},
        "study_time": {"type": "string"},
        "class_failures": {"type": "string"},
        "school_support": {"type": "string"},
        "family_support": {"type": "string"},
        "extra_paid_classes": {"type": "string"},
        "activities": {"type": "string"},
        "nursery_school": {"type": "string"},
        "higher_ed": {"type": "string"},
        "internet_access": {"type": "string"},
        "romantic_relationship": {"type": "string"},
        "family_relationship": {"type": "string"},
        "free_time": {"type": "string"},
        "social": {"type": "string"},
        "weekday_alcohol": {"type": "string"},
        "weekend_alcohol": {"type": "string"},
        "health": {"type": "string"},
        "absences": {"type": "string"}
    },
    "additionalProperties": False
}

schema_students_score = {
    "type": "object",
    "properties": {
        "student_id": {"type": "string"},
        "math_grade1": {"type": "string"},
        "math_grade2": {"type": "string"},
        "math_final_grade": {"type": "string"},
        "portuguese_grade1": {"type": "string"},
        "portuguese_grade2": {"type": "string"},
        "portuguese_final_grade": {"type": "string"}
    },
    "additionalProperties": False
}

schema_group = {
    "type": "object",
    "properties": {
        "columns_togroup": {"type": "string"},
        "column_toagg": {"type": "string"},
        "aggregate": {"type": "string"},
        "conditions": {"type": "string"}
    },
    "required": ["columns_togroup"],
    "additionalProperties": False
}

schema_join = {
    "type": "object",
    "properties": {
        "table1": {"type": "string"},
        "table2": {"type": "string"},
        "columns": {"type": "string"},
        "join_column": {"type": "string"},
        "conditions": {"type": "string"}
    },
    "required": ["table1", "table2", "join_column"],
    "additionalProperties": False
}
