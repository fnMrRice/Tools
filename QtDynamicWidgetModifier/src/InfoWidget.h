#ifndef INFOWIDGET_H
#define INFOWIDGET_H

#include <QWidget>

class QTableWidgetItem;

namespace Ui {
class InfoWidget;
}

class InfoWidget : public QWidget {
    Q_OBJECT

   public:
    explicit InfoWidget(QWidget *parent = nullptr);
    ~InfoWidget();

   public slots:
    void slot_onWidgetChanged(const std::vector<QWidget *> &widgets);

   private slots:
    void slot_onWidgetSelected(const int &index);
    void slot_onAttrModified(QTableWidgetItem *item);

   signals:
    void signal_startClicked();
    void signal_stopClicked();
    void signal_widgetSelected(int);

   private:
    Ui::InfoWidget *ui;
    std::vector<QWidget *> m_widgets;
    QWidget *m_selected = nullptr;
};

#endif  // INFOWIDGET_H
