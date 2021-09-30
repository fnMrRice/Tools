#include "include/WidgetModifier.h"

#include "CoverWidget.h"
#include "InfoWidget.h"

WidgetModifier::WidgetModifier(QWidget *watched, QObject *parent) : QObject(parent) {
    m_cover = new CoverWidget(watched);
    m_dialog = new InfoWidget(nullptr);

    connect(m_dialog, &InfoWidget::signal_startClicked,
            m_cover, &CoverWidget::start);
    connect(m_dialog, &InfoWidget::signal_stopClicked,
            m_cover, &CoverWidget::stop);
    connect(m_dialog, &InfoWidget::signal_widgetSelected,
            m_cover, &CoverWidget::slot_onWidgetSelected);
    connect(m_cover, &CoverWidget::signal_widgetChanged,
            m_dialog, &InfoWidget::slot_onWidgetChanged);

    m_dialog->show();
}
