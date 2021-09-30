#include "CoverWidget.h"

#include <QApplication>
#include <QDebug>
#include <QEvent>
#include <QPaintEvent>
#include <QPainter>
#include <list>

CoverWidget::CoverWidget(QWidget *parent) : QWidget(parent) {
    parent->installEventFilter(this);
    this->setAttribute(Qt::WidgetAttribute::WA_TransparentForMouseEvents, true);
}

void CoverWidget::start() {
    this->setMouseTracking(true);
    this->raise();
    this->setAttribute(Qt::WidgetAttribute::WA_TransparentForMouseEvents, false);
    m_started = true;
    update();
}

void CoverWidget::stop() {
    m_started = false;
    this->setMouseTracking(true);
    this->setAttribute(Qt::WidgetAttribute::WA_TransparentForMouseEvents, true);
    update();
}

bool CoverWidget::event(QEvent *event) {
    switch (event->type()) {
        case QEvent::ParentAboutToChange:
            if (auto p = this->parent()) {
                p->removeEventFilter(this);
            }
            break;
        case QEvent::ParentChange:
            if (auto p = this->parent()) {
                p->installEventFilter(this);
            }
            break;
        default:
            break;
    }
    return QWidget::event(event);
}

bool CoverWidget::eventFilter(QObject *watched, QEvent *event) {
    if (watched == this->parent()) {
        switch (event->type()) {
            case QEvent::Show:
            case QEvent::Resize:
                this->move(0, 0);
                this->setFixedSize(parentWidget()->width(), parentWidget()->height());
                break;
            default:
                break;
        }
    }
    return QWidget::eventFilter(watched, event);
}

void CoverWidget::paintEvent(QPaintEvent *e) {
    if (!m_started) return;
    auto painter = new QPainter(this);
    painter->setPen(Qt::NoPen);
    painter->setBrush(QColor(120, 120, 120, 120));
    painter->drawRect(e->rect());
    if (m_topWidget) {
        QPen pen;
        pen.setColor(Qt::green);
        pen.setWidth(2);
        painter->setPen(pen);
        painter->setBrush(Qt::NoBrush);
        painter->drawRect(m_topWidget->geometry());
    }
    if (m_selectedWidget) {
        QPen pen;
        pen.setColor(Qt::blue);
        pen.setWidth(2);
        painter->setPen(pen);
        painter->setBrush(Qt::NoBrush);
        painter->drawRect(m_selectedWidget->geometry());
    }
    delete painter;
}

void CoverWidget::mouseMoveEvent(QMouseEvent *) {
    if (!m_started) return;
    this->setAttribute(Qt::WA_TransparentForMouseEvents, true);

    auto w = QApplication::widgetAt(QCursor::pos());
    if (w != this->parentWidget()) {
        m_topWidget = w;
    } else {
        m_topWidget = nullptr;
    }

    this->setAttribute(Qt::WA_TransparentForMouseEvents, false);
    update();
}

void CoverWidget::mousePressEvent(QMouseEvent *) {
    if (!m_started) return;

    this->setAttribute(Qt::WA_TransparentForMouseEvents, true);

    auto backup = m_currentWidgets;
    m_currentWidgets.clear();
    while (auto w = QApplication::widgetAt(QCursor::pos())) {
        if (w == this->parentWidget()) break;
        m_currentWidgets.push_back(w);
        w->setAttribute(Qt::WA_TransparentForMouseEvents, true);
    }
    for (auto const &w : m_currentWidgets) {
        w->setAttribute(Qt::WA_TransparentForMouseEvents, false);
    }

    this->setAttribute(Qt::WA_TransparentForMouseEvents, false);
    if (m_currentWidgets.empty()) {
        m_currentWidgets = backup;
    } else {
        emit signal_widgetChanged(m_currentWidgets);
    }
}

void CoverWidget::slot_onWidgetSelected(const int &index) {
    if (index < 0) {
        m_selectedWidget = nullptr;
    }
    if ((size_t)index < m_currentWidgets.size()) {
        m_selectedWidget = m_currentWidgets.at(index);
    } else {
        m_selectedWidget = nullptr;
    }
    update();
}
