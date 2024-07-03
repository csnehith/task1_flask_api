"""Schemas"""

schema_student_details = {
    "type": "object",
    "properties": {
        "student_id": {"type": "number"},
        "school": {"type": "string"},
        "sex": {"type": "string"},
        "age": {"type": "number"},
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
        "class_failures": {"type": "number"},
        "school_support": {"type": "string"},
        "family_support": {"type": "string"},
        "extra_paid_classes": {"type": "string"},
        "activities": {"type": "string"},
        "nursery_school": {"type": "string"},
        "higher_ed": {"type": "string"},
        "internet_access": {"type": "string"},
        "romantic_relationship": {"type": "string"},
        "family_relationship": {"type": "number"},
        "free_time": {"type": "number"},
        "social": {"type": "number"},
        "weekday_alcohol": {"type": "number"},
        "weekend_alcohol": {"type": "number"},
        "health": {"type": "number"},
        "absences": {"type": "number"}
    },
    "additionalProperties": False
}

schema_students_score = {
    "type": "object",
    "properties": {
        "student_id": {"type": "number"},
        "math_grade1": {"type": "number"},
        "math_grade2": {"type": "number"},
        "math_final_grade": {"type": "number"},
        "portuguese_grade1": {"type": "number"},
        "portuguese_grade2": {"type": "number"},
        "portuguese_final_grade": {"type": "number"}
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
