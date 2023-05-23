import matplotlib.pyplot as plt
import matplotlib


matplotlib.use('Agg')


class Diagram:
    @staticmethod
    def generate(numbers_dict):
        x = numbers_dict.keys()
        y = numbers_dict.values()

        fig, ax = plt.subplots()
        ax.bar(x, y, color='lightblue')
        ax.set_facecolor('#000102')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.set_xlabel('Price', color='white')
        ax.set_ylabel('Count', color='white')
        ax.set_title(f'Anonymous numbers at different prices (top 10)', color='white')
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x, rotation=45, color='white')
        ax.grid(False)

        for i, v in enumerate(y):
            ax.annotate(str(v), xy=(i, v), ha='center', va='bottom', color='white')

        plt.subplots_adjust(bottom=0.15)  # Увеличение отступа снизу

        plt.savefig('diagram.png', facecolor='#000102')
        plt.close()

