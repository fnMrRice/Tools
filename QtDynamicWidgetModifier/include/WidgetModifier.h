#ifndef WIDGETMODIFIER_H
#define WIDGETMODIFIER_H

#include <QObject>

class CoverWidget;
class InfoWidget;

class WidgetModifier : public QObject {
    Q_OBJECT
   public:
    explicit WidgetModifier(QWidget *watched, QObject *parent = nullptr);

   private:
    CoverWidget *m_cover = nullptr;
    InfoWidget *m_dialog = nullptr;
};

#endif  // WIDGETMODIFIER_H
