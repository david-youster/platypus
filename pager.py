from flask import url_for

class Pager:

    def __init__(self, current_page, total_pages):
        self.current_page = int(current_page)
        self.total_pages = int(total_pages)

    def __str__(self):
        return '{} {} {}'.format(
            self.render_previous_link(),
            self.render_page_number(),
            self.render_next_link())

    def render_previous_link(self):
        if self.current_page <= 1:
            return ''
        href = url_for('index', page=self.current_page-1)
        return '<a href="{}">Previous</a>'.format(href)

    def render_page_number(self):
        return '{}/{}'.format(self.current_page, self.total_pages)

    def render_next_link(self):
        if self.current_page >= self.total_pages:
            return ''
        href = url_for('index', page=self.current_page+1)
        return '<a href="{}">Next</a>'.format(href)
