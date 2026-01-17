// Canvas setup
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game state
let gameRunning = false;
let gamePaused = false;
let score = 0;
let lives = 3;

// Ball properties
let balls = [];
const ballRadius = 8;
let destroyedCount = 0;

// Paddle properties
const paddle = {
    width: 75,
    height: 10,
    x: (canvas.width - 75) / 2,
    speed: 7
};

// Keyboard state
const keys = {
    left: false,
    right: false,
    space: false
};

// Bricks
const brickRowCount = 5;
const brickColumnCount = 7;
const brickWidth = 60;
const brickHeight = 20;
const brickPadding = 5;
const brickOffsetTop = 30;
const brickOffsetLeft = 15;

const bricks = [];
const brickColors = ['#e74c3c', '#e67e22', '#f39c12', '#2ecc71', '#3498db'];

function initBricks() {
    bricks.length = 0;
    for (let c = 0; c < brickColumnCount; c++) {
        bricks[c] = [];
        for (let r = 0; r < brickRowCount; r++) {
            bricks[c][r] = {
                x: 0,
                y: 0,
                status: 1,
                color: brickColors[r]
            };
        }
    }
}

// Event listeners
document.addEventListener('keydown', keyDownHandler);
document.addEventListener('keyup', keyUpHandler);
document.getElementById('startBtn').addEventListener('click', startGame);
document.getElementById('pauseBtn').addEventListener('click', togglePause);
document.getElementById('resetBtn').addEventListener('click', resetGame);

function keyDownHandler(e) {
    if (e.key === 'ArrowRight' || e.key === 'Right') {
        keys.right = true;
    } else if (e.key === 'ArrowLeft' || e.key === 'Left') {
        keys.left = true;
    } else if (e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        keys.space = true;
        if (gameRunning) {
            balls.forEach(ball => {
                if (!ball.launched) ball.launched = true;
            });
        }
    }
}

function keyUpHandler(e) {
    if (e.key === 'ArrowRight' || e.key === 'Right') {
        keys.right = false;
    } else if (e.key === 'ArrowLeft' || e.key === 'Left') {
        keys.left = false;
    } else if (e.key === ' ' || e.key === 'Spacebar') {
        keys.space = false;
    }
}

function drawBalls() {
    balls.forEach(ball => {
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();
        ctx.closePath();
    });
}

function drawPaddle() {
    ctx.beginPath();
    ctx.rect(paddle.x, canvas.height - paddle.height - 5, paddle.width, paddle.height);
    ctx.fillStyle = '#0095DD';
    ctx.fill();
    ctx.closePath();
}

function drawBricks() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            if (bricks[c][r].status === 1) {
                const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                ctx.beginPath();
                ctx.rect(brickX, brickY, brickWidth, brickHeight);
                ctx.fillStyle = bricks[c][r].color;
                ctx.fill();
                ctx.closePath();
            }
        }
    }
}

function collisionDetection() {
    balls.forEach(ball => {
        for (let c = 0; c < brickColumnCount; c++) {
            for (let r = 0; r < brickRowCount; r++) {
                const b = bricks[c][r];
                if (b.status === 1) {
                    if (ball.x > b.x && ball.x < b.x + brickWidth &&
                        ball.y > b.y && ball.y < b.y + brickHeight) {
                        ball.dy = -ball.dy;
                        b.status = 0;
                        score += 10;
                        destroyedCount++;
                        updateScore();

                        if (destroyedCount % 3 === 0) {
                            addNewBall(ball);
                        }

                        // Check win condition
                        if (score === brickRowCount * brickColumnCount * 10) {
                            alert('おめでとうございます！全てのブロックを破壊しました！');
                            resetGame();
                        }
                    }
                }
            }
        }
    });
}

function addNewBall(sourceBall) {
    balls.push({
        x: sourceBall.x,
        y: sourceBall.y,
        radius: ballRadius,
        dx: -sourceBall.dx,
        dy: sourceBall.dy,
        launched: true
    });
}

function updateScore() {
    document.getElementById('score').textContent = score;
}

function updateLives() {
    document.getElementById('lives').textContent = lives;
}

function movePaddle() {
    if (keys.right && paddle.x < canvas.width - paddle.width) {
        paddle.x += paddle.speed;
    }
    if (keys.left && paddle.x > 0) {
        paddle.x -= paddle.speed;
    }
}

function moveBalls() {
    balls.forEach(ball => {
        if (!ball.launched) {
            // Ball follows paddle before launch
            ball.x = paddle.x + paddle.width / 2;
            ball.y = canvas.height - paddle.height - 5 - ball.radius;
            return;
        }

        ball.x += ball.dx;
        ball.y += ball.dy;

        // Wall collision (left/right)
        if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
            ball.dx = -ball.dx;
        }

        // Wall collision (top)
        if (ball.y - ball.radius < 0) {
            ball.dy = -ball.dy;
        }

        // Paddle collision
        if (ball.y + ball.radius > canvas.height - paddle.height - 5) {
            if (ball.x > paddle.x && ball.x < paddle.x + paddle.width) {
                // Add angle based on where ball hits paddle
                const hitPos = (ball.x - paddle.x) / paddle.width;
                const angle = (hitPos - 0.5) * Math.PI / 3; // -60 to +60 degrees
                const speed = Math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy);
                ball.dx = speed * Math.sin(angle);
                ball.dy = -speed * Math.cos(angle);
            }
        }
    });

    // Remove balls that fell out
    balls = balls.filter(ball => ball.y - ball.radius < canvas.height);

    if (balls.length === 0 && gameRunning) {
        lives--;
        updateLives();

        if (lives === 0) {
            alert('ゲームオーバー！最終スコア: ' + score);
            resetGame();
        } else {
            resetBall();
        }
    }
}

function resetBall() {
    balls = [{
        x: paddle.x + paddle.width / 2,
        y: canvas.height - paddle.height - 5 - ballRadius,
        radius: ballRadius,
        dx: 3,
        dy: -3,
        launched: false
    }];
}

function draw() {
    if (!gameRunning || gamePaused) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw everything
    drawBricks();
    drawBalls();
    drawPaddle();
    collisionDetection();
    movePaddle();
    moveBalls();

    requestAnimationFrame(draw);
}

function startGame() {
    if (!gameRunning) {
        gameRunning = true;
        gamePaused = false;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        draw();
    }
}

function togglePause() {
    gamePaused = !gamePaused;
    document.getElementById('pauseBtn').textContent = gamePaused ? '再開' : '一時停止';
    if (!gamePaused) {
        draw();
    }
}

function resetGame() {
    gameRunning = false;
    gamePaused = false;
    score = 0;
    destroyedCount = 0;
    lives = 3;
    paddle.x = (canvas.width - paddle.width) / 2;
    resetBall();
    initBricks();
    updateScore();
    updateLives();
    document.getElementById('startBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('pauseBtn').textContent = '一時停止';

    // Draw initial state
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBricks();
    drawBall();
    drawPaddle();
}

// Initialize on load
resetBall();
initBricks();
ctx.clearRect(0, 0, canvas.width, canvas.height);
drawBricks();
drawBalls();
drawPaddle();
