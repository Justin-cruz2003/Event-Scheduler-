

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date

from models import db, Event, Resource, EventResourceAllocation

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    return render_template('base.html')


# ---------------- EVENTS ----------------
@app.route('/events')
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)


@app.route('/events/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not start_date or not end_date:
            return "Start date and End date are required", 400

        # Convert date → datetime (00:00 start, 23:59 end)
        start_time = datetime.strptime(start_date, '%Y-%m-%d')
        end_time = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59)

        event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events'))

    return render_template('add_event.html')


@app.route('/events/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.title = request.form['title']
        event.description = request.form['description']

        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not start_date or not end_date:
            return "Start date and End date are required", 400

        event.start_time = datetime.strptime(start_date, '%Y-%m-%d')
        event.end_time = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59)

        db.session.commit()
        return redirect(url_for('events'))

    return render_template('add_event.html', event=event)


# ---------------- RESOURCES ----------------
@app.route('/resources')
def resources():
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)


@app.route('/resources/add', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        name = request.form['name']
        rtype = request.form['type']

        resource = Resource(resource_name=name, resource_type=rtype)
        db.session.add(resource)
        db.session.commit()
        return redirect(url_for('resources'))

    return render_template('add_resource.html')


@app.route('/delete_event/<int:event_id>', methods=['POST', 'GET'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('events'))


@app.route('/delete_resource/<int:resource_id>', methods=['POST', 'GET'])
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    return redirect(url_for('resources'))


# ---------------- ALLOCATION + CONFLICT ----------------
@app.route('/allocate', methods=['GET', 'POST'])
def allocate_resource():
    events = Event.query.all()
    resources = Resource.query.all()
    error = None

    if request.method == 'POST':
        event_id = int(request.form['event_id'])
        resource_id = int(request.form['resource_id'])

        event = Event.query.get(event_id)

        conflicting_allocations = (
            EventResourceAllocation.query
            .join(Event)
            .filter(
                EventResourceAllocation.resource_id == resource_id,
                Event.start_time < event.end_time,
                Event.end_time > event.start_time
            ).all()
        )

        if conflicting_allocations:
            error = "This resource is already booked for another event during this time."
        else:
            allocation = EventResourceAllocation(
                event_id=event_id,
                resource_id=resource_id
            )
            db.session.add(allocation)
            db.session.commit()
            return redirect(url_for('view_allocations'))

    return render_template(
        'allocate.html',
        events=events,
        resources=resources,
        error=error
    )


@app.route('/allocations')
def view_allocations():
    allocations = EventResourceAllocation.query.all()
    return render_template('allocations.html', allocations=allocations)


# ---------------- STEP 5: UTILIZATION REPORT ----------------
@app.route('/report', methods=['GET', 'POST'])
def utilization_report():
    report_data = []
    start_date = end_date = None

    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

        resources = Resource.query.all()

        for resource in resources:
            total_hours = 0
            bookings = 0
            upcoming = 0

            for alloc in resource.allocations:
                event = alloc.event
                event_date = event.start_time.date()

                # In selected range
                if start_date <= event_date <= end_date:
                    duration = (event.end_time - event.start_time).total_seconds() / 3600
                    total_hours += duration
                    bookings += 1

                # Future events
                if event.start_time.date() > date.today():
                    upcoming += 1

            report_data.append({
                'name': resource.resource_name,
                'type': resource.resource_type,
                'hours': round(total_hours, 2),
                'bookings': bookings,
                'upcoming': upcoming
            })

    return render_template(
        'report.html',
        report_data=report_data,
        start_date=start_date,
        end_date=end_date
    )


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
