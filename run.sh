#!/bin/bash

python delay_histogram.py results/*
python score_histogram.py results/*
python overhead_request_response_histogram.py results/*
python wasted_time.py results/*
python gantt_chart.py results/*
python duration.py results/*
