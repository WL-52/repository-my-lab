#include <ncurses.h>
#include <chrono>
#include <thread>
#include <random>
#include <cmath>
#include <string>
#include <cstdlib>
#include <algorithm>

struct Paddle {
    double y;
    double x;
    int height;
};

struct Ball {
    double y;
    double x;
    double vy;
    double vx;
};

class PongGame {
public:
    PongGame(int rows, int cols, bool aiOpponent)
        : rows_(rows), cols_(cols), aiOpponent_(aiOpponent),
          rng_(static_cast<unsigned>(std::random_device{}())) {
        leftPaddle_  = {rows_ / 2.0 - 2.0, 2.0, 5};
        rightPaddle_ = {rows_ / 2.0 - 2.0, static_cast<double>(cols_ - 3), 5};
        resetBall(serveLeft_);
    }

    void handleInput(int ch) {
        switch (ch) {
            case 'w': case 'W': leftPaddle_.y  -= 1.5; break;
            case 's': case 'S': leftPaddle_.y  += 1.5; break;
            case KEY_UP:        rightPaddle_.y -= 1.5; break;
            case KEY_DOWN:      rightPaddle_.y += 1.5; break;
            case 'p': case 'P': paused_ = !paused_;    break;
            case 'r': case 'R':
                scoreLeft_ = scoreRight_ = 0;
                serveLeft_ = true;
                resetBall(true);
                gameOver_ = false;
                break;
        }
        clampPaddle(leftPaddle_);
        clampPaddle(rightPaddle_);
    }

    void update() {
        if (paused_ || gameOver_) return;

        if (aiOpponent_) {
            const double target = ball_.y - rightPaddle_.height / 2.0;
            const double diff = target - rightPaddle_.y;
            const double speed = 0.55;
            if (std::abs(diff) > 0.3) {
                rightPaddle_.y += (diff > 0 ? speed : -speed);
            }
            clampPaddle(rightPaddle_);
        }

        ball_.y += ball_.vy;
        ball_.x += ball_.vx;

        if (ball_.y <= 1.0) {
            ball_.y = 1.0;
            ball_.vy = -ball_.vy;
        } else if (ball_.y >= rows_ - 4) {
            ball_.y = rows_ - 4;
            ball_.vy = -ball_.vy;
        }

        bouncePaddle(leftPaddle_, true);
        bouncePaddle(rightPaddle_, false);

        if (ball_.x < 0) {
            scoreRight_ += 1;
            serveLeft_ = false;
            checkWin();
            resetBall(false);
        } else if (ball_.x > cols_ - 1) {
            scoreLeft_ += 1;
            serveLeft_ = true;
            checkWin();
            resetBall(true);
        }
    }

    void render() const {
        erase();

        for (int x = 0; x < cols_; ++x) {
            mvaddch(0, x, '=');
            mvaddch(rows_ - 3, x, '=');
        }
        for (int y = 1; y < rows_ - 3; ++y) {
            if (y % 2 == 0) mvaddch(y, cols_ / 2, '|');
        }

        attron(COLOR_PAIR(1));
        drawPaddle(leftPaddle_);
        drawPaddle(rightPaddle_);
        attroff(COLOR_PAIR(1));

        attron(COLOR_PAIR(2));
        mvaddch(static_cast<int>(ball_.y), static_cast<int>(ball_.x), 'O');
        attroff(COLOR_PAIR(2));

        std::string title = aiOpponent_ ? " PONG  (PvAI) " : " PONG  (PvP) ";
        mvprintw(0, std::max(0, cols_ / 2 - static_cast<int>(title.size()) / 2), "%s", title.c_str());
        mvprintw(rows_ - 2, 2, "P1 (W/S): %d   P2 (%s): %d",
                 scoreLeft_, aiOpponent_ ? "AI" : "Up/Down", scoreRight_);
        mvprintw(rows_ - 1, 2, "P - pause | R - restart | Q - quit  |  First to 7 wins");

        if (paused_)   mvprintw(rows_ / 2, cols_ / 2 - 4, " PAUSED ");
        if (gameOver_) {
            const std::string msg = winnerLeft_ ? " PLAYER 1 WINS! " : (aiOpponent_ ? " AI WINS! " : " PLAYER 2 WINS! ");
            mvprintw(rows_ / 2, std::max(0, cols_ / 2 - static_cast<int>(msg.size()) / 2), "%s", msg.c_str());
            mvprintw(rows_ / 2 + 1, cols_ / 2 - 9, "Press R to restart");
        }
        refresh();
    }

private:
    void clampPaddle(Paddle& p) const {
        if (p.y < 1) p.y = 1;
        if (p.y + p.height > rows_ - 3) p.y = rows_ - 3 - p.height;
    }

    void drawPaddle(const Paddle& p) const {
        for (int i = 0; i < p.height; ++i) {
            mvaddch(static_cast<int>(p.y) + i, static_cast<int>(p.x), '|');
        }
    }

    void bouncePaddle(const Paddle& p, bool leftSide) {
        const int by = static_cast<int>(ball_.y);
        const int bx = static_cast<int>(ball_.x);
        if (bx == static_cast<int>(p.x) &&
            by >= static_cast<int>(p.y) &&
            by <  static_cast<int>(p.y) + p.height) {
            const double hit = (ball_.y - p.y) / static_cast<double>(p.height) - 0.5;
            const double speed = std::min(1.4, std::hypot(ball_.vx, ball_.vy) + 0.05);
            const double angle = hit * 1.0;
            ball_.vx = (leftSide ? 1.0 : -1.0) * speed * std::cos(angle);
            ball_.vy = speed * std::sin(angle) + hit * 0.4;
            ball_.x  = p.x + (leftSide ? 1.0 : -1.0);
        }
    }

    void resetBall(bool toLeft) {
        ball_.y = rows_ / 2.0;
        ball_.x = cols_ / 2.0;
        std::uniform_real_distribution<double> ang(-0.4, 0.4);
        const double a = ang(rng_);
        const double speed = 0.6;
        ball_.vx = (toLeft ? -1.0 : 1.0) * speed * std::cos(a);
        ball_.vy = speed * std::sin(a);
    }

    void checkWin() {
        const int target = 7;
        if (scoreLeft_ >= target)  { gameOver_ = true; winnerLeft_ = true; }
        if (scoreRight_ >= target) { gameOver_ = true; winnerLeft_ = false; }
    }

    int rows_;
    int cols_;
    bool aiOpponent_;
    Paddle leftPaddle_{};
    Paddle rightPaddle_{};
    Ball ball_{};
    int scoreLeft_  = 0;
    int scoreRight_ = 0;
    bool paused_    = false;
    bool gameOver_  = false;
    bool winnerLeft_ = false;
    bool serveLeft_  = true;
    std::mt19937 rng_;
};

static int chooseMode() {
    clear();
    mvprintw(2, 4, "PONG");
    mvprintw(4, 4, "1) Player vs AI");
    mvprintw(5, 4, "2) Player vs Player");
    mvprintw(7, 4, "Choose mode (1/2): ");
    refresh();
    nodelay(stdscr, FALSE);
    int ch;
    while (true) {
        ch = getch();
        if (ch == '1' || ch == '2') break;
        if (ch == 'q' || ch == 'Q') return 0;
    }
    nodelay(stdscr, TRUE);
    return ch == '1' ? 1 : 2;
}

int main() {
    initscr();
    if (!has_colors()) {
        endwin();
        fprintf(stderr, "Your terminal does not support colors.\n");
        return 1;
    }
    start_color();
    use_default_colors();
    init_pair(1, COLOR_CYAN, -1);
    init_pair(2, COLOR_YELLOW, -1);

    cbreak();
    noecho();
    curs_set(0);
    keypad(stdscr, TRUE);
    nodelay(stdscr, TRUE);

    const int mode = chooseMode();
    if (mode == 0) { endwin(); return 0; }

    int rows = 0;
    int cols = 0;
    getmaxyx(stdscr, rows, cols);
    if (rows < 12) rows = 24;
    if (cols < 40) cols = 80;

    PongGame game(rows, cols, mode == 1);

    using clock = std::chrono::steady_clock;
    auto lastTick = clock::now();
    const auto tick = std::chrono::milliseconds(40);

    while (true) {
        int ch = getch();
        if (ch == 'q' || ch == 'Q') break;
        if (ch != ERR) game.handleInput(ch);

        auto now = clock::now();
        if (now - lastTick >= tick) {
            game.update();
            lastTick = now;
        }

        game.render();
        std::this_thread::sleep_for(std::chrono::milliseconds(8));
    }

    endwin();
    return 0;
}
