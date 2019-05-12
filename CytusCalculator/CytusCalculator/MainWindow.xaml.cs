using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace CytusCalculator
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        private int PerfectCount = 0, GoodCount = 0, BadCount = 0, MissCount = 0;
        private double TP;
        private TextBox PerfectBox, GoodBox, BadBox, MissBox, TPBox;
        private VisualBrush PerfectBrush, GoodBrush, BadBrush, MissBrush, TPBrush;
        public MainWindow() {
            InitializeComponent();
            setResult();

            SolidColorBrush foreGroundColor = new SolidColorBrush(Color.FromArgb(255, 217, 217, 217));
            SolidColorBrush transparentBrush = new SolidColorBrush(Color.FromArgb(0, 0, 0, 0));
            PerfectBox = new TextBox() {
                Text = "Perfect Count",
                Foreground = foreGroundColor,
                Background = transparentBrush,
                BorderBrush = transparentBrush
            };
            PerfectBrush = new VisualBrush() { Opacity = 0.5, Stretch = Stretch.None, AlignmentX = AlignmentX.Right, Visual = PerfectBox };
            PerfectInput.Background = PerfectBrush;

            GoodBox = new TextBox() {
                Text = "Good Count",
                Foreground = foreGroundColor,
                Background = transparentBrush,
                BorderBrush = transparentBrush
            };
            GoodBrush = new VisualBrush() { Opacity = 0.5, Stretch = Stretch.None, AlignmentX = AlignmentX.Right, Visual = GoodBox };
            GoodInput.Background = GoodBrush;

            BadBox = new TextBox() {
                Text = "Bad Count",
                Foreground = foreGroundColor,
                Background = transparentBrush,
                BorderBrush = transparentBrush
            };
            BadBrush = new VisualBrush() { Opacity = 0.5, Stretch = Stretch.None, AlignmentX = AlignmentX.Right, Visual = BadBox };
            BadInput.Background = BadBrush;

            MissBox = new TextBox() {
                Text = "Miss Count",
                Foreground = foreGroundColor,
                Background = transparentBrush,
                BorderBrush = transparentBrush
            };
            MissBrush = new VisualBrush() { Opacity = 0.5, Stretch = Stretch.None, AlignmentX = AlignmentX.Right, Visual = MissBox };
            MissInput.Background = MissBrush;

            TPBox = new TextBox() {
                Text = "TP",
                Foreground = foreGroundColor,
                Background = transparentBrush,
                BorderBrush = transparentBrush
            };
            TPBrush = new VisualBrush() { Opacity = 0.5, Stretch = Stretch.None, AlignmentX = AlignmentX.Right, Visual = TPBox };
            TPInput.Background = TPBrush;
        }

        private void setResult(int pureCount, int total) {
            FlowDocument doc = new FlowDocument();
            Paragraph p = new Paragraph();
            Run pure = new Run() { Text = Convert.ToString(pureCount), Foreground = new SolidColorBrush(Color.FromRgb(255, 255, 0)) };
            Run notPure=new Run() { Text=Convert.ToString(total-pureCount), Foreground = new SolidColorBrush(Color.FromRgb(255, 255, 150)) };
            Run plus = new Run(" + ");

            p.Inlines.Add(pure);
            p.Inlines.Add(plus);
            p.Inlines.Add(notPure);
            p.Padding = new Thickness(2);

            doc.Blocks.Add(p);
            doc.TextAlignment = TextAlignment.Right;
            Result1Text.Document = doc;
        }

        private void setResult() {
            FlowDocument doc = new FlowDocument();
            Paragraph p = new Paragraph();
            Run r = new Run() { Text = "0", Foreground = new SolidColorBrush(Color.FromRgb(0, 0, 0)) };

            p.Inlines.Add(r);
            p.Padding = new Thickness(2);
            doc.Blocks.Add(p);
            doc.TextAlignment = TextAlignment.Right;
            
            Result1Text.Document = doc;
        }

        private void On_PerfectLabelClick(object sender, MouseButtonEventArgs e) {
            PerfectInput.Focus();
        }

        private void On_GoodLabelClick(object sender, MouseButtonEventArgs e) {
            GoodInput.Focus();
        }

        private void On_BadLabelClick(object sender, MouseButtonEventArgs e) {
            BadInput.Focus();
        }

        private void On_MissLabelClick(object sender, MouseButtonEventArgs e) {
            MissInput.Focus();
        }

        private void On_InputKeyDown(object sender, KeyEventArgs e) { // 判断输入是否为数字
            bool shiftKey = (Keyboard.Modifiers & ModifierKeys.Shift) != 0;//判断shifu键是否按下
            if (shiftKey == true) { //当按下shift
                e.Handled = true; //不可输入
            } else { //未按shift
                if (!(
                        (e.Key >= Key.D0 && e.Key <= Key.D9) ||  // 0-9
                        (e.Key >= Key.NumPad0 && e.Key <= Key.NumPad9) || // NumPad 0-9
                        e.Key == Key.Delete || // Delete
                        e.Key == Key.Back || // BackSpace
                        e.Key == Key.Left || // Left
                        e.Key == Key.Right || // Right
                        e.Key == Key.Tab) // Tab
                    ) {
                    e.Handled = true; //不可输入
                }
            }
        }

        private void On_InputKeyDown_WithDot(object sender, KeyEventArgs e) { // 判断输入是否为小数
            // (100(\.(00?)?)?)|([0-9]{1,2}(\.[0-9]{0,2})?)
            bool shiftKey = (Keyboard.Modifiers & ModifierKeys.Shift) != 0;//判断shifu键是否按下
            if (shiftKey == true) { //当按下shift
                e.Handled = true; //不可输入
            } else { //未按shift
                if (!(
                        (e.Key >= Key.D0 && e.Key <= Key.D9) ||  // 0-9
                        (e.Key >= Key.NumPad0 && e.Key <= Key.NumPad9) || // NumPad 0-9
                        e.Key == Key.Decimal || // Dot
                        e.Key == Key.Delete || // Delete
                        e.Key == Key.Back || // BackSpace
                        e.Key == Key.Left || // Left
                        e.Key == Key.Right || // Right
                        e.Key == Key.Tab) // Tab
                    ) {
                    e.Handled = true; //不可输入
                }
                TextBox textBox = (TextBox)sender;
                if (e.Key == Key.Decimal && textBox.Text.Length == 0) {
                    textBox.Text = "0.";
                    textBox.SelectionStart = 2;
                    e.Handled = true;
                }
                if (e.Key == Key.Decimal && textBox.Text.IndexOf(".") != -1) e.Handled = true;
            }
        }

        private void Calculate() {
            // TP = (100*Perfect + 70*Perfect2 + 30*Good) / All Count
            // 100*x + 70*(P-x) + 30*G = TP*All
            // 30*x = TP*All - 70*P - 30*G
            int All = PerfectCount + GoodCount + BadCount + MissCount;
            int PurePerfect = Convert.ToInt16((TP * All - PerfectCount * 70 - 30 * GoodCount) / 30);
            if (PurePerfect > PerfectCount) { setResult(); return; }
            if (PurePerfect < 0) { setResult(); return; }
            //Result1Text.Text = Convert.ToString(PurePerfect);
            setResult(PurePerfect, PerfectCount);
        }

        private void On_PerfectInputChanged(object sender, TextChangedEventArgs e) {
            try {
                if (PerfectInput.Text.Length==0) {
                    PerfectInput.Background = PerfectBrush;
                    return;
                }

                PerfectInput.Background = null;
                PerfectCount = Convert.ToInt32(PerfectInput.Text);
                Calculate();
            } catch (Exception) {
                GoodCount = 0;
            }
        }

        private void On_GoodInputChanged(object sender, TextChangedEventArgs e) {
            try {
                if (GoodInput.Text.Length == 0) {
                    GoodInput.Background = GoodBrush;
                    return;
                }

                GoodInput.Background = null;
                GoodCount = Convert.ToInt32(GoodInput.Text);
                Calculate();
            } catch(Exception) {
                GoodCount = 0;
            }
        }

        private void On_BadInputChanged(object sender, TextChangedEventArgs e) {
            try {
                if (BadInput.Text.Length == 0) {
                    BadInput.Background = BadBrush;
                    return;
                }

                BadInput.Background = null;
                BadCount = Convert.ToInt32(BadInput.Text);
                Calculate();
            } catch (Exception) {
                GoodCount = 0;
            }
        }

        private void On_MissInputChanged(object sender, TextChangedEventArgs e) {
            try {
                if (MissInput.Text.Length == 0) {
                    MissInput.Background = MissBrush;
                    return;
                }

                MissInput.Background = null;
                MissCount = Convert.ToInt32(MissInput.Text);
                Calculate();
            } catch (Exception) {
                GoodCount = 0;
            }
        }

        private void On_TPInputChanged(object sender, TextChangedEventArgs e) {
            try {
                if (TPInput.Text.Length == 0) {
                    TPInput.Background = TPBrush;
                    return;
                }

                TPInput.Background = null;
                TP = Convert.ToDouble(TPInput.Text);
                Calculate();
            } catch (Exception) {
                TP = 0;
            }
        }

    }
}
