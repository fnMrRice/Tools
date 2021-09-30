#ifndef TESTWIDGET_H
#define TESTWIDGET_H

#include <QWidget>

class WidgetModifier;

QT_BEGIN_NAMESPACE
namespace Ui {
class TestWidget;
}
QT_END_NAMESPACE

class TestWidget : public QWidget {
    Q_OBJECT

   public:
    TestWidget(QWidget *parent = nullptr);
    ~TestWidget();

   private:
    Ui::TestWidget *ui;
    WidgetModifier *m_modifier = nullptr;
};
#endif  // TESTWIDGET_H
