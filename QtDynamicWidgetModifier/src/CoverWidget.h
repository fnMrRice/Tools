#ifndef COVERWIDGET_H
#define COVERWIDGET_H

#include <QWidget>

class CoverWidget : public QWidget {
    Q_OBJECT
   public:
    explicit CoverWidget(QWidget *parent = nullptr);

   public slots:
    void start();
    void stop();

   protected:
    bool event(QEvent *event) override;
    bool eventFilter(QObject *watched, QEvent *event) override;
    void paintEvent(QPaintEvent *) override;
    void mouseMoveEvent(QMouseEvent *) override;
    void mousePressEvent(QMouseEvent *) override;

   public slots:
    void slot_onWidgetSelected(const int &index);

   signals:
    void signal_widgetChanged(const std::vector<QWidget *> &widgets);

   private:
    bool m_started = false;
    QWidget *m_topWidget = nullptr;
    std::vector<QWidget *> m_currentWidgets;
    QWidget *m_selectedWidget = nullptr;
};

#endif  // COVERWIDGET_H
