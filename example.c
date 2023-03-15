#include <raylib.h>

int
main(void)
{
    InitWindow(640, 480, "EXAMPLE");
    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);

        char const* const text = "RAYLIB WINDOW IN C";
        int const font_size = 20;
        int text_width = MeasureText(text, font_size);
        int text_height = GetFontDefault().baseSize;
        int text_x = GetScreenWidth() / 2 - text_width / 2;
        int text_y = GetScreenHeight() / 2 - text_height;
        DrawText(text, text_x, text_y, font_size, LIGHTGRAY);

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
