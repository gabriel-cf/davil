"""
    Table generator
"""

# TODO - Extend from AbstractWidget

from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource

class TableGenerator(object):
    """Generator of data tables widgets"""

    @staticmethod
    def init_table(view):
        """Generates the info table"""
        dimension_values_df = view.get_dimension_values_df()
        source = ColumnDataSource(dimension_values_df)
        source.add(dimension_values_df.index, name='name')
        columns = [TableColumn(field=field, title=field)
                   for field in dimension_values_df.columns.values]
        columns.insert(0, TableColumn(field='name', title='name'))
        data_table = DataTable(source=source, columns=columns, width=1000, height=600)
        return data_table