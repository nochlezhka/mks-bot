import matplotlib
import six
import matplotlib.pyplot as plt
import io


def render_mpl_table(columns, data, font_size=14,
                     header_color='#B4B4B3', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1.5, 1.5], header_columns=0,
                     ax=None, **kwargs):
    mpl_table = ax.table(
        cellText=data, bbox=bbox,
        colLabels=columns, **kwargs,
        loc='center',
        cellLoc='center'
    )

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):

        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_text_props(wrap=True)
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
            try:
                cell_data = data[k[0] - 1][k[1]]

                if cell_data == "fail":
                    cell.set_facecolor("#FFA8A8")
                elif cell_data == "ok":
                    cell.set_facecolor("#B6FFCE")
                elif cell_data == "?":
                    cell.set_facecolor("#F6FFA4")
            except Exception as ex:
                print(ex)

    return ax


def convert(header, data):
    matplotlib.pyplot.switch_backend('Agg')

    fig, ax = plt.subplots(figsize=(18, 6))
    ax.axis('tight')
    ax.axis('off')

    ax = render_mpl_table(header, data, ax=ax)

    buffer = io.BytesIO()

    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    image_data = buffer.read()

    plt.close(fig)
    buffer.close()

    return image_data
